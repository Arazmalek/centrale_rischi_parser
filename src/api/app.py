import os
import uuid
import threading
import logging
from flask import Flask, jsonify, request
import sys

# Add source directories to Python path for internal imports
# CRITICAL: This allows the API layer to find the core and storage modules
# Note: You may need to create __init__.py files in these folders for the import to work.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../storage')))

# Import modules from our own project structure
from parser_engine import FinancialReportParser
from aws_utils import upload_file_to_s3, save_result_to_dynamo, send_webhook_notification

# Configure logging for the application (Professional Standard)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration loaded from environment variables
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "./temp_uploads")
BASE_WEBHOOK_URL = os.environ.get("DEFAULT_WEBHOOK_URL", "http://localhost:5000/webhook")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- ASYNCHRONOUS PROCESSING LOGIC ---

def process_document_background(file_path: str, request_id: str, webhook_url: str):
    """
    Background thread to handle the long-running parsing task.
    Prevents the API call from timing out.
    """
    # Initialize the core parser
    parser = FinancialReportParser()
    
    try:
        logger.info(f"Processing started for Request ID: {request_id}")
        
        # 1. Execute the Core Parsing Logic
        parsing_results = parser.process_document(file_path)
        
        # 2. Save Results and Final Status to Storage (DynamoDB/S3)
        save_result_to_dynamo(request_id, "DONE", parsing_results)
        
        # 3. Notify Client via Webhook
        send_webhook_notification(webhook_url, request_id, "finished")
        logger.info(f"Parsing and notification completed for {request_id}")

    except Exception as e:
        error_message = str(e)
        logger.error(f"Error processing {request_id}: {error_message}", exc_info=True)
        # On failure, log error status to DB and notify client
        save_result_to_dynamo(request_id, "ERROR", error_msg=error_message)
        send_webhook_notification(webhook_url, request_id, "error", error_message)
        
    finally:
        # Crucial: Always clean up local files
        if os.path.exists(file_path):
            os.remove(file_path)

# --- API ENDPOINT ---

@app.route('/cr_parse', methods=['POST'])
def cr_parse_endpoint():
    """
    Main API endpoint to receive PDF via POST request (form-data).
    """
    # 1. Input Validation
    if 'file' not in request.files or not request.files['file'].filename:
        return jsonify({'error': 'No valid file provided in the request.'}), 400
        
    file = request.files['file']
    client_webhook = request.form.get('webhook_url', BASE_WEBHOOK_URL)

    # 2. Setup Unique IDs and File Paths
    request_id = str(uuid.uuid4())
    safe_filename = f"{request_id}.pdf"
    # Note: Using UPLOAD_FOLDER from environment variables
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    
    try:
        # Save file temporarily on the local container volume
        file.save(file_path)
        
        # 3. Store Raw File in S3 for backup/audit trail
        upload_file_to_s3(file_path, safe_filename)
        
        # 4. Initialize Status in DynamoDB
        save_result_to_dynamo(request_id, "PROCESSING")
        
        # 5. Start ASYNC Processing
        thread = threading.Thread(
            target=process_document_background, 
            args=(file_path, request_id, client_webhook)
        )
        thread.start()

        # 6. Immediate Response to Client
        return jsonify({
            'statusCode': 200,
            'Request_Id': request_id,
            'message': 'File accepted and processing started asynchronously.'
        })

    except Exception as e:
        logger.critical(f"Fatal error during API ingestion: {e}")
        return jsonify({'error': 'Internal Server Error during ingestion process.'}), 500

if __name__ == '__main__':
    # Production deployment will use Gunicorn/Nginx
    app.run(host='0.0.0.0', port=5000)
