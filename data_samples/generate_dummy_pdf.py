import os
from fpdf import FPDF

# --- Configuration ---
# The script will output the test PDF here
OUTPUT_DIR = "data_samples"
PDF_FILENAME = "test_financial_report.pdf"

class CustomPDF(FPDF):
    """PDF class customized for generating financial report structure."""
    
    def header(self):
        """Adds a professional header to the top of the PDF."""
        self.set_font('Arial', 'B', 12)
        # Title matches the financial domain
        self.cell(0, 10, 'SYNTHETIC FINANCIAL REPORT - DUMMY DATA', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        """Adds page numbering to the bottom."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_structured_dummy_file():
    """Generates the structured PDF file for parser testing."""
    pdf = CustomPDF()
    pdf.add_page()
    
    # 1. Metadata Headers (Crucial for regex testing in parser_engine)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, "DATA DI RIFERIMENTO: 01/2025", 0, 1) # Target for date parsing
    pdf.cell(0, 5, "Intestatario: SYNTHETIC CORP, INC.", 0, 1) # Target for header parsing
    pdf.cell(0, 5, "Codice Fiscale: 99999999999", 0, 1) # Target for VAT/Fiscale parsing
    pdf.ln(8)
    
    # 2. Table Header (The structure the parser must extract)
    pdf.set_font('Arial', 'B', 9)
    col_width = 38
    headers = ['Intermediario', 'Tipo di Rapporto', 'Stato', 'Importo Finale (EUR)']
    
    for header in headers:
        pdf.cell(col_width, 8, header, 1, 0, 'C')
    pdf.ln()
    
    # 3. Dummy Data Rows
    pdf.set_font('Arial', '', 9)
    dummy_data = [
        ['Test Bank Alpha', 'Fido', 'Accordato', '150,000.00'],
        ['Demo Credit Beta', 'Mutuo', 'Utilizzato', '75,000.00'],
        ['Financial Mockup', 'Leasing', 'Residuo', '20,500.00'],
        ['Risk Free Co.', 'Linea BT', 'Chiuso', '0.00'],
    ]
    
    for row in dummy_data:
        for item in row:
            pdf.cell(col_width, 8, item, 1, 0, 'C')
        pdf.ln()

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    pdf.output(os.path.join(OUTPUT_DIR, PDF_FILENAME))
    print(f"\n[SUCCESS] Dummy PDF created at: {OUTPUT_DIR}/{PDF_FILENAME}")

if __name__ == "__main__":
    # Note: Requires 'fpdf' library to run locally.
    create_structured_dummy_file()
