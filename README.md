# 🏦 Centrale Rischi Financial Data Parser (Secure & Scalable)

## 📋 Executive Summary
This repository hosts a production-grade, containerized data extraction engine designed to parse complex, multi-page financial PDF reports (specifically *Centrale Rischi* documents). The solution automates the extraction of critical financial indicators, tabular data, and metadata, transforming unstructured PDF content into structured, queryable datasets.

**Key Achievement:**
Engineered to process high volumes of financial documents with precision, this parser handles dynamic table structures, multi-page layouts, and data normalization, significantly reducing manual data entry efforts.

---

## 🏗️ Architecture & Workflow

The system is architected as a modular microservice, leveraging **Docker** for portability and ease of deployment.

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
git clone [https://github.com/YOUR_USERNAME/cr-parser-pro.git](https://github.com/YOUR_USERNAME/cr-parser-pro.git)
cd cr-parser-pro
