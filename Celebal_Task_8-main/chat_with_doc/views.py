import os
import time
from django.shortcuts import render
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings  
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize LLM and Prompt
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
prompt = ChatPromptTemplate.from_template("""
Answer the questions based on the provided context only.
<context>
{context}
<context>
Question: {input}
""")

# Constants
MAX_PDF_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_PAGE_COUNT = 100

import asyncio  # ADD this

def vector_embedding(uploaded_files):
    import asyncio
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    os.makedirs("uploaded_documents", exist_ok=True)

    all_docs = []
    for file in uploaded_files:
        if file.size > MAX_PDF_SIZE:
            return f"{file.name} exceeds 50 MB limit."

        try:
            pdf_reader = PdfReader(file)
            if len(pdf_reader.pages) > MAX_PAGE_COUNT:
                return f"{file.name} exceeds 100 page limit."
        except Exception as e:
            return f"Error reading {file.name}: {e}"

        file.seek(0)
        path = os.path.join("uploaded_documents", file.name)
        with open(path, "wb") as f:
            f.write(file.read())

        docs = PyPDFLoader(path).load()
        all_docs.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(all_docs)

    global vectors
    vectors = FAISS.from_documents(split_docs, embeddings)
    return "Your document is ready to take your questions."


def document_chat_view(request):
    context = {}
    if "pdf_names" not in request.session:
        request.session["pdf_names"] = []

    if request.method == "POST":
        if "upload" in request.POST:
            uploaded_files = request.FILES.getlist("pdf_files")
            if uploaded_files:
                msg = vector_embedding(uploaded_files)
                if msg.startswith("Your document"):
                    request.session["pdf_names"] = [f.name for f in uploaded_files]
                    context.update({"message": msg, "pdf_names": request.session["pdf_names"]})
                else:
                    context["error"] = msg
            else:
                context["error"] = "Please upload at least one PDF."

        elif "ask" in request.POST:
            question = request.POST.get("question")
            context["pdf_names"] = request.session.get("pdf_names", [])

            if question and "vectors" in globals():
                chain = create_retrieval_chain(vectors.as_retriever(), create_stuff_documents_chain(llm, prompt))
                start = time.process_time()
                response = chain.invoke({'input': question})
                elapsed = time.process_time() - start

                context.update({
                    "response": response.get("answer", "No answer generated."),
                    "response_time": elapsed,
                    "question": question,
                    "documents": [doc.page_content for doc in response.get("context", [])]
                })
            else:
                context["error"] = "Question missing or documents not ready."

    return render(request, "Doc_Chat.html", context)
