import os
import sqlite3
from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import google.auth
import jwt


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

#default is session if it does not find 'SESSION_COOKIE_NAME'
app.config['SESSION_COOKIE_NAME'] = os.getenv('SESSION_COOKIE_NAME', 'session')

# Set up OAuth 2.0 credentials

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

if google_client_id and google_client_secret:
    print("Google OAuth credentials are loaded successfully!")
else:
    print("Google OAuth credentials are not set!")


# Set up OAuth Flow
flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": os.getenv('GOOGLE_CLIENT_ID'),
            "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:5000/callback"]  # Ensure this matches
        }
    },
    scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"]
)


def get_db_connection():
    conn = sqlite3.connect('thunder.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/sign_up', methods=['POST'])
def sign_up():
    username = request.form['username']
    password = hash_password(request.form['password'])
    email = request.form['email']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
    ''', (username, password, email))
    conn.commit()
    conn.close
    
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'google_id' in session:
        return f'Logged in as {session["google_id"]}'
    return redirect(url_for('login'))

@app.route('/login')
def login():
    flow.redirect_uri = url_for('callback', _external=True) # Explicitly set the redirect URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt = 'consent'
        )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/profile')
def profile():
    if 'google_id' not in session:
        return redirect(url_for('login'))
    
    # Fetch user details from the database
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE google_id = ?', (session['google_id'],)).fetchone()
    conn.close()

    return f'Hello, {user["email"]}'


@app.route('/callback')
def callback():
    print("Request args:", request.args)  # Log the query parameters
    
    # Handle errors
    if 'error' in request.args:
        return f"Error: {request.args['error']}"
    
    if 'code' not in request.args:
        return "Missing authorization code!"
    
    # Verify the state parameter to prevent CSRF
    if 'state' not in request.args or request.args['state'] != session.get('state'):
        return "State mismatch. Potential CSRF detected!", 400
    
    try:
        # Fetch the token using the authorization response
        flow.fetch_token(authorization_response=request.url)

        # Get the credentials from the flow
        credentials = flow.credentials

        # Decode the id_token (JWT)
        id_token_dict = jwt.decode(credentials.id_token, options={"verify_signature": False})
        
        # Now you can access the user information from the decoded token
        google_id = id_token_dict['sub']
        email = id_token_dict['email']
        
        # Store or update the user in the database
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE google_id = ?', (google_id,)).fetchone()
        
        if not user:
            # User doesn't exist, so insert them into the database
            conn.execute('''
                INSERT INTO users (google_id, email, username, sign_in_count)
                VALUES (?, ?, ?, 1)
            ''', (google_id, email, email))  # Using email as the username
            conn.commit()
        else:
            # User exists, so update their sign-in count
            conn.execute('''
                UPDATE users
                SET sign_in_count = sign_in_count + 1
                WHERE google_id = ?
            ''', (google_id,))
            conn.commit()

        # Store the google_id in session to indicate that the user is logged in
        session['google_id'] = google_id
        conn.close()

        return redirect(url_for('home'))
    
    except Exception as e:
        return f"Error during OAuth callback: {e}", 400

@app.route('/logout')
def logout():
    session.pop('google_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
