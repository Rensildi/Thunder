import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class BusinessPlanPDFGenerator:
    def __init__(self, business_plan_data):
        self.business_plan_data = business_plan_data
        self.pdf_buffer = BytesIO()
    
    def generate_pdf(self):
        """Generate the PDF"""
        doc = SimpleDocTemplate(self.pdf_buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Title Style
        title_style = styles['Title']
        title_style.fontSize = 18
        title_style.leading = 22

        # Paragraph with indentation
        normal_style = ParagraphStyle(name='Normal', fontSize=10, leading=12, spaceBefore=6, spaceAfter=6)
        normal_style.firstLineIndent = 20  # Indentation for body paragraphs

        # Title
        title = Paragraph("Business Plan", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Create sections
        elements.extend(self.create_section("Industry", 3, normal_style))
        elements.extend(self.create_section("Employees", 4, normal_style))
        elements.extend(self.create_section("Legal Structure", 5, normal_style))
        elements.extend(self.create_section("Description", 2, normal_style))
        elements.extend(self.create_section("Mission Statement", 3, normal_style))
        elements.extend(self.create_section("Principal Members", 4, normal_style))
        elements.extend(self.create_section("Future", 5, normal_style))
        
        elements.extend(self.create_section("Industry State", 2, normal_style))
        elements.extend(self.create_section("Competitors", 3, normal_style))
        elements.extend(self.create_section("Target Audience", 4, normal_style))
        elements.extend(self.create_section("Company Advantages", 5, normal_style))
        elements.extend(self.create_section("Regulations Compliance", 6, normal_style))

        elements.extend(self.create_section("Growth Strategy", 2, normal_style))
        elements.extend(self.create_section("Advertising Plan", 3, normal_style))
        elements.extend(self.create_section("Marketing Budget", 4, normal_style))
        elements.extend(self.create_section("Customer Interaction", 5, normal_style))
        elements.extend(self.create_section("Customer Retention", 6, normal_style))

        elements.extend(self.create_section("Products", 2, normal_style))
        elements.extend(self.create_section("Services", 3, normal_style))
        elements.extend(self.create_section("Pricing", 4, normal_style))
        elements.extend(self.create_section("Research", 5, normal_style))

        elements.extend(self.create_section("Name", 2, normal_style))
        elements.extend(self.create_section("Address", 3, normal_style))
        elements.extend(self.create_section("City", 4, normal_style))
        elements.extend(self.create_section("State", 5, normal_style))
        elements.extend(self.create_section("Zip Code", 6, normal_style))
        elements.extend(self.create_section("Phone", 7, normal_style))
        elements.extend(self.create_section("Email", 8, normal_style))

        elements.extend(self.create_section("Financing Sought", 2, normal_style))
        elements.extend(self.create_section("Profit and Loss Statement", 3, normal_style))
        elements.extend(self.create_section("Break-even Analysis", 4, normal_style))
        elements.extend(self.create_section("Return on Investment (ROI)", 5, normal_style))
        elements.extend(self.create_section("Contingency Plan", 6, normal_style))
        elements.extend(self.create_section("Disaster Recovery Plan", 7, normal_style))
        elements.extend(self.create_section("Bank", 8, normal_style))
        elements.extend(self.create_section("Accounting Firm", 9, normal_style))
        elements.extend(self.create_section("Insurance Info", 10, normal_style))

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

    def create_section(self, section_name, index, style):
        """Create a section with title and body text"""
        title_style = ParagraphStyle(name='Title', fontSize=14, leading=16, spaceAfter=4)
        title_style.fontName = 'Helvetica-Bold'

        # Initialize with empty value
        section_data = ""

        # Access data based on the section_name and index
        if section_name == "Industry":
            section_data = self.business_plan_data['business_plans'][3]
        elif section_name == "Employees":
            section_data = self.business_plan_data['business_plans'][4]
        elif section_name == "Legal Structure":
            section_data = self.business_plan_data['business_plans'][5]
        elif section_name == "Description":
            section_data = self.business_plan_data['executive_summary'][2]
        elif section_name == "Mission Statement":
            section_data = self.business_plan_data['executive_summary'][3]
        elif section_name == "Principal Members":
            section_data = self.business_plan_data['executive_summary'][4]
        elif section_name == "Future":
            section_data = self.business_plan_data['executive_summary'][5]
        elif section_name == "Industry State":
            section_data = self.business_plan_data['market_research'][2]
        elif section_name == "Competitors":
            section_data = self.business_plan_data['market_research'][3]
        elif section_name == "Target Audience":
            section_data = self.business_plan_data['market_research'][4]
        elif section_name == "Company Advantages":
            section_data = self.business_plan_data['market_research'][5]
        elif section_name == "Regulations Compliance":
            section_data = self.business_plan_data['market_research'][6]
        elif section_name == "Growth Strategy":
            section_data = self.business_plan_data['marketing_strategy'][2]
        elif section_name == "Advertising Plan":
            section_data = self.business_plan_data['marketing_strategy'][3]
        elif section_name == "Marketing Budget":
            section_data = self.business_plan_data['marketing_strategy'][4]
        elif section_name == "Customer Interaction":
            section_data = self.business_plan_data['marketing_strategy'][5]
        elif section_name == "Customer Retention":
            section_data = self.business_plan_data['marketing_strategy'][6]
        elif section_name == "Products":
            section_data = self.business_plan_data['service_line'][2]
        elif section_name == "Services":
            section_data = self.business_plan_data['service_line'][3]
        elif section_name == "Pricing":
            section_data = self.business_plan_data['service_line'][4]
        elif section_name == "Research":
            section_data = self.business_plan_data['service_line'][5]
        elif section_name == "Name":
            section_data = self.business_plan_data['contact_information'][2]
        elif section_name == "Address":
            section_data = self.business_plan_data['contact_information'][3]
        elif section_name == "City":
            section_data = self.business_plan_data['contact_information'][4]
        elif section_name == "State":
            section_data = self.business_plan_data['contact_information'][5]
        elif section_name == "Zip Code":
            section_data = self.business_plan_data['contact_information'][6]
        elif section_name == "Phone":
            section_data = self.business_plan_data['contact_information'][7]
        elif section_name == "Email":
            section_data = self.business_plan_data['contact_information'][8]
        elif section_name == "Financing Sought":
            section_data = self.business_plan_data['financial'][2]
        elif section_name == "Profit and Loss Statement":
            section_data = self.business_plan_data['financial'][3]
        elif section_name == "Break-even Analysis":
            section_data = self.business_plan_data['financial'][4]
        elif section_name == "Return on Investment (ROI)":
            section_data = self.business_plan_data['financial'][5]
        elif section_name == "Contingency Plan":
            section_data = self.business_plan_data['financial'][6]
        elif section_name == "Disaster Recovery Plan":
            section_data = self.business_plan_data['financial'][7]
        elif section_name == "Bank":
            section_data = self.business_plan_data['financial'][8]
        elif section_name == "Accounting Firm":
            section_data = self.business_plan_data['financial'][9]
        elif section_name == "Insurance Info":
            section_data = self.business_plan_data['financial'][10]

        # Skip this section if the data is empty
        if section_data == "":
            return [] 

        # If data is not empty create section 
        title = Paragraph(f"<b>{section_name}:</b>", title_style)
        body = Paragraph(f"{section_data}", style)

        return [title, body, Spacer(1, 12)]


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
