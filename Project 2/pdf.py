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

        industry = Paragraph(f"<b>Industry:</b><br/> {self.business_plan_data['business_plans'][3] if self.business_plan_data['business_plans'] is not None else ''}", styles['Normal'])
        employees = Paragraph(f"<b>Employees:</b><br/> {self.business_plan_data['business_plans'][4] if self.business_plan_data['business_plans'] is not None else ''}", styles['Normal'])
        legal_structure = Paragraph(f"<b>Legal Structure:</b><br/> {self.business_plan_data['business_plans'][5] if self.business_plan_data['business_plans'] is not None else ''}", styles['Normal'])

        description = Paragraph(f"<b>Description:</b><br/> {self.business_plan_data['executive_summary'][2] if self.business_plan_data['executive_summary'] is not None else ''}", styles['Normal'])
        mission_statement = Paragraph(f"<b>Mission Statement:</b><br/> {self.business_plan_data['executive_summary'][3] if self.business_plan_data['executive_summary'] is not None else ''}", styles['Normal'])
        principal_members = Paragraph(f"<b>Principal Members:</b><br/> {self.business_plan_data['executive_summary'][4] if self.business_plan_data['executive_summary'] is not None else ''}", styles['Normal'])
        future = Paragraph(f"<b>Future:</b><br/> {self.business_plan_data['executive_summary'][5] if self.business_plan_data['executive_summary'] and self.business_plan_data['executive_summary'][5] is not None else ''}", styles['Normal'])

        industry_state = Paragraph(f"<b>Industry State:</b><br/> {self.business_plan_data['market_research'][2] if self.business_plan_data['market_research'] is not None else ''}", styles['Normal'])
        competitors = Paragraph(f"<b>Competitors:</b><br/> {self.business_plan_data['market_research'][3] if self.business_plan_data['market_research'] is not None else ''}", styles['Normal'])
        target_audience = Paragraph(f"<b>Target Audience:</b><br/> {self.business_plan_data['market_research'][4] if self.business_plan_data['market_research'] is not None else ''}", styles['Normal'])
        company_advantages = Paragraph(f"<b>Company Advantages:</b><br/> {self.business_plan_data['market_research'][5] if self.business_plan_data['market_research'] is not None else ''}", styles['Normal'])
        regulations_compliance = Paragraph(f"<b>Regulations Compliance:</b><br/> {self.business_plan_data['market_research'][6] if self.business_plan_data['market_research'] is not None else ''}", styles['Normal'])

        growth_strategy = Paragraph(f"<b>Growth Strategy:</b><br/> {self.business_plan_data['marketing_strategy'][2] if self.business_plan_data['marketing_strategy'] is not None else ''}", styles['Normal'])
        advertising_plan = Paragraph(f"<b>Advertising Plan:</b><br/> {self.business_plan_data['marketing_strategy'][3] if self.business_plan_data['marketing_strategy'] is not None else ''}", styles['Normal'])
        marketing_budget = Paragraph(f"<b>Marketing Budget:</b><br/> {self.business_plan_data['marketing_strategy'][4] if self.business_plan_data['marketing_strategy'] is not None else ''}", styles['Normal'])
        customer_interaction = Paragraph(f"<b>Customer Interaction:</b><br/> {self.business_plan_data['marketing_strategy'][5] if self.business_plan_data['marketing_strategy'] is not None else ''}", styles['Normal'])
        customer_retention = Paragraph(f"<b>Customer Retention:</b><br/> {self.business_plan_data['marketing_strategy'][6] if self.business_plan_data['marketing_strategy'] is not None else ''}", styles['Normal'])

        products = Paragraph(f"<b>Products:</b><br/> {self.business_plan_data['service_line'][2] if self.business_plan_data['service_line'] is not None else ''}", styles['Normal'])
        services = Paragraph(f"<b>Services:</b><br/> {self.business_plan_data['service_line'][3] if self.business_plan_data['service_line'] is not None else ''}", styles['Normal'])
        pricing = Paragraph(f"<b>Pricing:</b><br/> {self.business_plan_data['service_line'][4] if self.business_plan_data['service_line'] is not None else ''}", styles['Normal'])
        research = Paragraph(f"<b>Research:</b><br/> {self.business_plan_data['service_line'][5] if self.business_plan_data['service_line'] is not None else ''}", styles['Normal'])

        name = Paragraph(f"<b>Name:</b><br/> {self.business_plan_data['contact_information'][2] if self.business_plan_data['contact_information'] is not None else ''}", styles['Normal'])
        address = Paragraph(f"<b>Address:</b><br/> {self.business_plan_data['contact_information'][3] if self.business_plan_data['contact_information'] is not None else ''}", styles['Normal'])
        city = Paragraph(f"<b>City:</b><br/> {self.business_plan_data['contact_information'][4] if self.business_plan_data['contact_information'] is not None else ''}", styles['Normal'])
        state = Paragraph(f"<b>State:</b><br/> {self.business_plan_data['contact_information'][5] if self.business_plan_data['contact_information'] is not None else ''}", styles['Normal'])
        zip_code = Paragraph(f"<b>Zip Code:</b><br/> {self.business_plan_data['contact_information'][6] if self.business_plan_data['contact_information'] is not None else ''}", styles['Normal'])
        phone = Paragraph(f"<b>Phone:</b><br/> {self.business_plan_data['contact_information'][7] if self.business_plan_data['contact_information'] is not None else ''}", styles['Normal'])
        email = Paragraph(f"<b>Email:</b><br/> {self.business_plan_data['contact_information'][8] if self.business_plan_data['contact_information'] is not None else ''}", styles['Normal'])

        financing_sought = Paragraph(f"<b>Financing Sought:</b><br/> {self.business_plan_data['financial'][2] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        profit_loss_statement = Paragraph(f"<b>Profit and Loss Statement:</b><br/> {self.business_plan_data['financial'][3] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        break_even_analysis = Paragraph(f"<b>Break-even Analysis:</b><br/> {self.business_plan_data['financial'][4] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        roi = Paragraph(f"<b>Return on Investment (ROI):</b><br/> {self.business_plan_data['financial'][5] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        contingency_plan = Paragraph(f"<b>Contingency Plan:</b><br/> {self.business_plan_data['financial'][6] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        disaster_recovery_plan = Paragraph(f"<b>Disaster Recovery Plan:</b><br/> {self.business_plan_data['financial'][7] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        bank = Paragraph(f"<b>Bank:</b><br/> {self.business_plan_data['financial'][8] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        accounting_firm = Paragraph(f"<b>Accounting Firm:</b><br/> {self.business_plan_data['financial'][9] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])
        insurance_info = Paragraph(f"<b>Insurance Info:</b><br/> {self.business_plan_data['financial'][10] if self.business_plan_data['financial'] is not None else ''}", styles['Normal'])

        # Append text to elements list
        elements.extend([
            industry, employees, legal_structure, 
            description, mission_statement, principal_members, future,
            industry_state, competitors, target_audience, company_advantages, regulations_compliance,
            growth_strategy, advertising_plan, marketing_budget, customer_interaction, customer_retention,
            products, services, pricing, research,
            name, address, city, state, zip_code, phone, email,
            financing_sought, profit_loss_statement, break_even_analysis, roi, contingency_plan, disaster_recovery_plan, bank, accounting_firm, insurance_info
        ])
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
    
    