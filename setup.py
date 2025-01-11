from setuptools import setup, find_packages

setup(
    name="pdf_qa_chatbot",
    version="0.1.0",
    description="A PDF Q&A Chatbot with RAG and image support",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Core Dependencies
        "streamlit==1.32.0",
        "PyMuPDF==1.23.8",
        "Pillow>=10.0.0",
        "python-dotenv==1.0.0",
        
        # LangChain and Related
        "langchain==0.1.0",
        "langchain-community==0.0.19",
        "chromadb==0.4.22",
        "sentence-transformers==2.3.1",
        
        # Utilities
        "requests>=2.31.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0"
    ]
)