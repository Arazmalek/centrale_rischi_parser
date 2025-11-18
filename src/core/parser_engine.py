import camelot
import fitz  # PyMuPDF
import os
import logging
import pandas as pd
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversionBackend(object):
    """
    Custom backend for Camelot to convert PDF pages to PNG using PyMuPDF (fitz).
    This serves as a lightweight alternative to Ghostscript.
    """
    def convert(self, pdf_path, png_path):
        try:
            # Determine output filename based on the PDF path
            output_name = os.path.splitext(pdf_path)[0] + '.png'
            doc = fitz.open(pdf_path)
            for page in doc:
                pix = page.get_pixmap()
                pix.save(output_name)
            logger.debug(f"Converted {pdf_path} to PNG for Camelot processing.")
        except Exception as e:
            logger.error(f"ConversionBackend Error: {e}")
            raise e

class FinancialReportParser:
    """
    Core engine for processing Financial Reports (Centrale Rischi).
    Handles layout detection, table extraction, and data cleaning.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _detect_page_orientation(self, file_path: str) -> bool:
        """
        Detects if the PDF page is Landscape or Portrait to optimize extraction coordinates.
        Returns: True if Landscape, False if Portrait.
        """
        try:
            doc = fitz.open(file_path)
            page = doc[0]
            rect = page.rect
            # If width > height, it's likely Landscape
            is_landscape = rect.width > rect.height
            self.logger.info(f"Page Orientation Detected: {'Landscape' if is_landscape else 'Portrait'}")
            return is_landscape
        except Exception as e:
            self.logger.warning(f"Could not detect orientation, defaulting to Portrait. Error: {e}")
            return False

    def parse_tables(self, file_path: str, pages: str = 'all') -> List[Any]:
        """
        Extracts tables from the PDF using Camelot's 'Lattice' mode.
        Lattice is optimized for tables with distinct grid lines, common in financial reports.
        """
        self.logger.info(f"Starting table extraction for: {file_path}")
        
        try:
            # Using the custom ConversionBackend for image processing
            tables = camelot.read_pdf(
                file_path, 
                backend=ConversionBackend(), 
                flavor='lattice',  
                line_scale=40,     # Adjust line detection sensitivity
                pages=pages
            )
            self.logger.info(f"Successfully extracted {len(tables)} tables.")
            return tables
            
        except Exception as e:
            self.logger.error(f"Critical Error during Camelot extraction: {e}")
            return []

    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Main entry point for the parser.
        Orchestrates layout detection, extraction, and data structuring.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # 1. Layout Analysis
        is_landscape = self._detect_page_orientation(file_path)
        
        # 2. Table Extraction
        raw_tables = self.parse_tables(file_path)
        
        processed_data = []
        
        # 3. Data Cleaning & Structuring
        for i, table in enumerate(raw_tables):
            df = table.df
            
            # Data Cleaning: Remove artifacts like newlines in cell text
            df = df.replace(r'\n', ' ', regex=True)
            
            # Convert DataFrame to list of dictionaries (JSON-serializable)
            table_records = df.to_dict(orient='records')
            
            # Enrich with metadata (Page number, Table confidence score)
            processed_data.append({
                "table_index": i,
                "page_number": table.parsing_report['page'],
                "content": table_records,
                "extraction_accuracy": table.parsing_report['accuracy']
            })
            
        return processed_data
