import re
from typing import List, Dict, Any, Generator

def chunker(sequence: List[Any], size: int) -> Generator[List[Any], None, None]:
    """
    Splits a large sequence (list of items) into smaller, fixed-size chunks.
    This is essential for batch processing or adhering to database limits (e.g., DynamoDB 400KB).
    """
    return (sequence[pos:pos + size] for pos in range(0, len(sequence), size))

def calculate_date_metadata(date_ref_str: str) -> Dict[str, str]:
    """
    Parses a reference date string (e.g., 'GENNAIO 2025') to extract month and year.
    Used for enriching extracted table data with metadata.
    """
    try:
        # Assuming the date format is "MONTH YEAR"
        month = date_ref_str.split(' ', 1)[0]
        year = date_ref_str.split(' ', 1)[1]
        return {'year': year, 'month': month}
    except Exception:
        # Returns None on failure, indicating incomplete metadata
        return {'year': "None", 'month': "None"}

def extract_clean_value(start_marker: str, end_marker: str, text: str) -> str:
    """
    Extracts a substring between two markers using regex.
    This logic is used to cleanly pull specific metadata (like CCIAA, Seduta Legale) 
    from the complex text layout of the financial PDF headers.
    """
    try:
        # Attempt to find text between start and end markers
        result = re.search(f'{re.escape(start_marker)}(.*?){re.escape(end_marker)}', text, re.IGNORECASE | re.DOTALL)
        if not result:
            # Fallback: Find text from start marker to end of string
            result = re.search(f'{re.escape(start_marker)}(.*)', text, re.IGNORECASE | re.DOTALL)
            
        if result:
            final_value = result.group(1).strip()
            return final_value
        return ""
    except Exception:
        return ""
