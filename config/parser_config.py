# This file holds abstract rules that define how to parse financial reports.

# --- METADATA EXTRACTION RULES ---
# Defines the regex patterns for the parser engine to find fixed headers (e.g., date, VAT number).
# The parser code will iterate through these rules.
METADATA_RULES = {
    "REFERENCE_DATE_PATTERN": r"DATA DI RIFERIMENTO:\s*(\d{2}/\d{4})",
    "COMPANY_HEADER_PATTERN": r"Intestatario:\s*(.*)",
    "VAT_CODE_PATTERN": r"Codice Fiscale:\s*(\d{11})",
    "ISSUE_DATE_PATTERN": r"Le informazioni sono disponibili a far tempo dal\s*(.*)",
}

# --- TABLE MAPPING RULES ---
# Defines the structure and key words needed for Camelot to crop tables correctly.
# This demonstrates configurable parsing architecture.
TABLE_RULES = [
    {
        "name": "TRANSACTION_SUMMARY",
        "keywords": ["DATA DI RIFERIMENTO", "IMPORTO", "RISCHIO"],
        "pages": "all",
        "extraction_method": "lattice"
    },
    {
        "name": "CREDIT_LINES_DETAIL",
        "keywords": ["TIPO DI RAPPORTO", "UTILIZZATO"],
        "pages": "2-5",
        "extraction_method": "stream"
    }
]
