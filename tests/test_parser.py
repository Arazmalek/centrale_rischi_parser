
import os
import sys
import json
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from io import BytesIO

# 1. Setup Path to find source code (CRITICAL)
# This allows the test runner to find the modules inside src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/core/utils')))


# --- Imports from the project's logic ---
# Ensure these match the files you created (parser_engine.py and data_utils.py)
from data_utils import chunker, extract_clean_value 
from parser_engine import FinancialReportParser 

# --- 2. Test Utility Functions (data_utils.py) ---

def test_chunker_remainder():
    """Verify chunker handles lists that do not divide evenly."""
    data = ['a', 'b', 'c', 'd', 'e']
    chunks = list(chunker(data, 2))
    assert len(chunks) == 3
    assert chunks[2] == ['e']

def test_extract_clean_value_success():
    """Verify regex extraction between two markers works correctly."""
    text = "Codice Fiscale: 12345678901 Codice Lei"
    result = extract_clean_value("Fiscale:", "Codice Lei", text)
    assert result == "12345678901"

def test_extract_clean_value_no_end_marker():
    """Verify regex extracts until the end if the end marker is not found."""
    text = "Intestatario: Mario Rossi S.R.L. End of text."
    result = extract_clean_value("Intestatario:", "NonExistent", text)
    assert "Mario Rossi S.R.L. End of text." in result 

# --- 3. Mock Test for Core Parser (parser_engine.py) ---

# We mock external dependencies (fitz/camelot) which are slow and heavy.
@patch('parser_engine.fitz.open')
@patch('parser_engine.camelot.read_pdf')
def test_parser_handles_file_not_found(mock_read_pdf, mock_fitz_open):
    """Verify the parser fails gracefully (raises FileNotFoundError) if the input file does not exist."""
    parser = FinancialReportParser()
    
    # Configure mock to simulate File Not Found error
    mock_fitz_open.side_effect = FileNotFoundError 
    
    with pytest.raises(FileNotFoundError):
        parser.process_document("/path/to/nonexistent/file.pdf")

@patch('parser_engine.FinancialReportParser.parse_tables')
def test_process_document_returns_correct_structure(mock_parse_tables):
    """Verify that the main process method returns the correct list structure with metadata."""
    
    # Mock the output of the complex Camelot parser (simulating a parsed table)
    mock_parse_tables.return_value = [
        MagicMock(
            df=pd.DataFrame({'Header1': ['A', 'B']}),
            parsing_report={'page': 1, 'accuracy': 95.0},
            _bbox=(0,0,0,0) # Bounding box property required by internal logic
        )
    ]
    
    parser = FinancialReportParser()
    # Run the function with a dummy path
    results = parser.process_document("dummy_path.pdf")
    
    # Assertions on the final aggregated structure
    assert isinstance(results, list)
    assert len(results) == 1
    assert "extraction_accuracy" in results[0]
    assert results[0]['page_number'] == 1
    assert isinstance(results[0]['content'], list) # Content should be a list of dicts
