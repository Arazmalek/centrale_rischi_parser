# 🏦 Centrale Rischi Financial Data Parser (Secure & Scalable)

## 📋 Executive Summary
This repository hosts a production-grade, containerized data extraction engine designed to parse complex, multi-page financial PDF reports (specifically *Centrale Rischi* documents). The solution automates the extraction of critical financial indicators, tabular data, and metadata, transforming unstructured PDF content into structured, queryable datasets.

**Key Achievement:**
Engineered to process high volumes of financial documents with precision, this parser handles dynamic table structures, multi-page layouts, and data normalization, significantly reducing manual data entry efforts.

---

## 🏗️ Architecture & Workflow

The system is architected as a modular microservice, leveraging **Docker** for portability and ease of deployment.


![cr_graph (1)](https://github.com/user-attachments/assets/74fce580-fc36-4ee6-ac99-9dc52e6ce065)


### Core Components:
1.  **Parser Engine (`src/core`):**
    * Utilizes **Camelot** (Lattice mode) for high-fidelity table extraction.
    * Integrates **PyMuPDF (Fitz)** for layout analysis, metadata extraction (headers, dates), and page orientation detection.
2.  **API Layer (`src/api`):**
    * A robust **Flask** API endpoint (`/parse_document`) handles file uploads and processing requests.
    * Implements asynchronous processing using threading to ensure API responsiveness.
3.  **Data Pipeline (`src/storage`):**
    * **S3 Integration:** Securely uploads raw PDF backups to AWS S3.
    * **DynamoDB Integration:** Stores structured parsing results and processing status in AWS DynamoDB.
4.  **Infrastructure (`docker/`):**
    * Fully containerized using **Docker**.
    * Deployed with **Gunicorn** as the WSGI HTTP server for production performance.
    * Includes **Nginx** configuration for reverse proxy handling.

---

## 🛠️ Technical Specifications

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core logic and scripting. |
| **Web Framework** | Flask | RESTful API for document submission. |
| **PDF Extraction** | Camelot-py, PyMuPDF (Fitz) | Table and text extraction logic. |
| **Cloud Services** | AWS S3, DynamoDB | Storage and NoSQL database for results. |
| **Containerization** | Docker & Docker Compose | Deployment consistency and isolation. |
| **Server** | Gunicorn & Nginx | Production-ready application serving. |

---

## 🚀 Setup & Installation

### Prerequisites
* Docker and Docker Compose installed.
* AWS Credentials configured (via Environment Variables).

### 1. Clone the Repository
```bash
git clone [https://github.com/Arazmalek/centrale_rischi_parser.git](https://github.com/Arazmalek/centrale_rischi_parser.git)
cd centrale_rischi_parser
```

### 2. Configuration
Create a `.env` file in the root directory (based on `.env.example`) and populate it with your credentials. **Note:** Never commit real credentials to Git.

```env
# .env example
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=eu-south-1
S3_BUCKET_NAME=your-bucket-name
DYNAMO_TABLE_NAME=your-table-name
```

### 3. Build and Run with Docker
```bash
docker-compose up --build
```
The API will be available at `http://localhost:80` (via Nginx) or `http://localhost:5000` (direct).

---

## 📖 Usage

### API Endpoint: `/parse_document`
* **Method:** `POST`
* **Payload:** `form-data` with a file field named `file`.

**Example Request (cURL):**
```bash
curl -X POST -F "file=@/path/to/sample_report.pdf" http://localhost/parse_document
```

**Response:**
```json
{
    "statusCode": 200,
    "request_id": "unique-uuid-v4",
    "message": "File accepted for processing."
}
```

---

## 🔒 Security & Disclaimer

> **⚠️ IMPORTANT DISCLAIMER:**
> * **Synthetic Data:** The PDF files provided in the `data_samples/` directory are **synthetically generated dummy documents**. No real financial data or Personally Identifiable Information (PII) from real clients is used, stored, or processed in this public repository.
> * **Credential Safety:** All sensitive configuration (AWS keys, DB endpoints) has been abstracted into environment variables. The code provided here is a sanitized version of the production system, designed for portfolio demonstration purposes.

---

**Araz Malekazari** | *Senior Data Engineer & System Architect*
