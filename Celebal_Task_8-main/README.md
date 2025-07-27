# DocumentChat - AI-Powered Document Question Answering System

## Overview

DocumentChat is a web application built with Django that allows users to upload PDF documents and ask questions about their content using natural language. The system leverages the Retrieval Augmented Generation (RAG) approach with FAISS vector database for efficient semantic search and LLM integration for generating accurate responses.

![DocumentChat Screenshot](https://via.placeholder.com/800x400?text=DocumentChat+Screenshot)

## Features

- **Document Upload**: Support for uploading multiple PDF documents
- **Vector Database**: FAISS-powered vector storage for efficient semantic search
- **Context-Aware AI**: Retrieves relevant document snippets and generates coherent responses
- **Real-time Interaction**: Ask questions in natural language and get immediate answers
- **Modern UI**: Clean, responsive interface with loading indicators and intuitive design
- **Document Management**: View all uploaded documents in one place

## Technology Stack

- **Backend Framework**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (document metadata) + FAISS (vector embeddings)
- **PDF Processing**: PyPDF2/pdf2text for text extraction
- **Embeddings**: Sentence Transformers/BERT embeddings for semantic search
- **LLM Integration**: Connection to LLM APIs for generating responses
- **Deployment**: Docker support for containerization

## Architecture

This application follows the Retrieval Augmented Generation (RAG) architecture:

1. **Document Processing Pipeline**:
   - PDF documents are uploaded and stored
   - Text is extracted and chunked into manageable segments
   - Text chunks are converted into vector embeddings
   - Vectors are stored in a FAISS index for efficient similarity search

2. **Question Answering Pipeline**:
   - User questions are converted to vector embeddings
   - FAISS performs similarity search to find relevant document chunks
   - Retrieved context is sent along with the question to the LLM
   - LLM generates a response based on the retrieved context

## Installation

### Prerequisites

- Python 3.9+
- Django 4.2+
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/ChitwanRana/document-chat.git
   cd document-chat
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv myenv
   # On Windows: myenv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```


## Usage

1. **Upload Documents**:
   - Navigate to the upload section
   - Select PDF files or drag and drop them
   - Click "Upload PDFs"

2. **Ask Questions**:
   - After documents are processed, go to the chat section
   - Type your question in the input field
   - Click "Ask" button or press Enter
   - View the AI-generated response based on your documents

## Project Structure

```
celebal/
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
├── celebal/               # Main Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py
├── chat_with_doc/         # Main application
│   ├── __init__.py
│   ├── admin.py           # Admin interface
│   ├── apps.py
│   ├── models.py          # Database models
│   ├── tests.py
│   ├── urls.py            # App-specific URLs
│   └── views.py           # View controllers
├── templates/             # HTML templates
│   └── Doc_Chat.html      # Main chat interface
└── uploaded_documents/    # Storage for uploaded PDFs
```

## Implementation Details

### Vector Database with FAISS

FAISS (Facebook AI Similarity Search) is used for efficient similarity search:
- Creates an index of document chunks for fast retrieval
- Supports cosine similarity search for semantic matching
- Scales efficiently with large document collections

### Text Chunking Strategy

Documents are processed into chunks for better context retrieval:
- Chunks overlap to preserve context across boundaries
- Chunk size is optimized for the LLM context window
- Metadata links chunks back to original documents

### LLM Integration

The system connects to LLM APIs for natural language processing:
- Provides relevant context from documents
- Uses prompt engineering for better response generation
- Handles response formatting for web display


## Future Improvements

- Multiple language support
- OCR integration for scanned documents
- User authentication and document permissions
- Document type expansion (support for DOCX, TXT, etc.)
- Chat history and session management
- Fine-tuning LLM for domain-specific responses
- Performance optimizations for large document collections

# Made with LOVE 💓 by Divyanshu Chaudhary
