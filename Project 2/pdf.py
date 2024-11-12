import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

class BusinessPlanPDFGenerator:
    def __init__(self, business_plan_data):
        self.business_plan_data = business_plan_data
        self.pdf_buffer = BytesIO()
    
    def generate_pdf(self):
        """Generate the PDF"""
        doc = SimpleDocTemplate(self.pdf_buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph("Business Plan", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Business plan text 
        description = Paragraph(f"<b>Description:</b><br/> {self.business_plan_data[0]}", styles['Normal'])
        goals = Paragraph(f"<b>Goals:</b><br/> {self.business_plan_data[1]}", styles['Normal'])
        target_audience = Paragraph(f"<b>Target Audience:</b><br/> {self.business_plan_data[2]}", styles['Normal'])

        # Append text to elements list
        elements.extend([description, goals, target_audience])
        elements.append(Spacer(1, 12))

        # Sample graph just to test inserting in pdf
        chart_image_stream = self.create_chart()

        # Add graph to the pdf
        chart_image = Image(chart_image_stream, width=300, height=200)
        elements.append(chart_image)
        
        # Create the pdf
        doc.build(elements)
        
        # Reset buffer 
        self.pdf_buffer.seek(0)
        
        return self.pdf_buffer

    def create_chart(self):
        """Generate a simple bar chart and save it to a BytesIO buffer"""
        # Sample data 
        data = [20, 20, 25, 25, 10]
        labels = ['Profit', 'Labor', 'Materials', 'Salaries', 'Overhead']
        
        fig, ax = plt.subplots()
        ax.bar(labels, data, color="#0066CC")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")
        ax.set_title("Sample Business Data Chart")
        
        # Save chart to a BytesIO object so it can be put directly into a pdf
        img_stream = BytesIO()
        plt.savefig(img_stream, format='png')
        plt.close()
        
        # Set BytesIO stream
        img_stream.seek(0)
        
        return img_stream
    
    