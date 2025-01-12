# ED-Chatbot: A Q&A System for PDF Documents
The ED-Chatbot is an intelligent question-and-answer system built to process and analyze PDF documents. Users can upload PDFs and interact with the system by asking questions about the document's content. The chatbot combines modern Natural Language Processing (NLP) techniques with an intuitive interface built using Streamlit, leveraging a Retrieval-Augmented Generation (RAG) model for accurate and context-aware responses.

## Features
**PDF Upload:** Users can upload PDF documents containing text or images for analysis.
**Question-Answer Interaction:** Provides accurate and context-specific answers based on PDF content.
**Semantic Search:** Utilizes vector embeddings to find and focus on the most relevant parts of the document.
**Dynamic User Interface:** Built with Streamlit, offering an intuitive and seamless experience.
**Image Support:** Handles PDFs containing embedded images and text.
**Reliability:** Uses retrieval-augmented generation to ground responses in the document content, reducing misinformation.

## Why This Model/Approach Was Chosen
### Why RAG Model Was Used
The chatbot uses a Retrieval-Augmented Generation (RAG) model, combining the strengths of retrieval-based and generative NLP techniques:

1. Dynamic Knowledge Retrieval:
- Retrieves relevant content from uploaded PDFs for real-time processing.
- Ensures responses are grounded in the provided document, making it highly accurate.

2. Minimizing Hallucinations:
- Reduces the likelihood of generating incorrect answers by grounding responses in retrieved content.

3. Scalable and Extensible:
- Efficiently handles large repositories of documents using dense vector embeddings.
- Future-proof design, easily adaptable to new data or models.

4. State-of-the-Art NLP Techniques:
- Embedding generation via Sentence-Transformers ensures precise similarity searches.
- Retrieval components integrated with ChromaDB enable scalable and fast query processing.

### Why Ollama Was Used
Ollama is a local LLM server that provides several advantages for this project:

1. Privacy and Security:
By running locally, sensitive data, such as the content of PDFs, does not leave the user's machine. This ensures compliance with privacy requirements.

2. Performance:
Local execution of models minimizes latency compared to cloud-based API calls. This makes the chatbot faster and more responsive.

3. Cost Efficiency:
Avoids recurring costs associated with cloud-based LLM APIs, such as OpenAI's GPT-4.

4. Flexibility:
Ollama supports custom and fine-tuned models that can be optimized for specific use cases, making it highly adaptable to diverse requirements.

While Ollama is primarily a local server, with proper configuration, it can be deployed to a cloud environment for remote access, making it suitable for future scalability.

## Installation
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd ED-chatbot
    ```
2. Setup virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install the required Python packages:
    ```bash
    pip install -e .
    ```    
4. Run the application:
    ```bash
    streamlit run main.py
    ```

### Key Technologies
**Streamlit:** For building a user-friendly interface.
**RAG Model:** Combines retrieval and generation for accurate responses.
**Ollama:** A local LLM server used to host and run advanced language models privately.
**PyMuPDF:** For extracting text and images from PDFs.
**ChromaDB:** For embedding storage and fast similarity searches.
**Sentence-Transformers:** For generating dense embeddings of text.
**Pillow:** For processing image data within PDFs.

### Future Enhancements
1. Cloud Deployment for Ollama:
- Ollama, while a local server, can be containerized using Docker and deployed on cloud platforms (e.g., AWS, Azure, or GCP) for global accessibility. This would allow the chatbot to operate in distributed environments while retaining its core functionalities.

2. Support for Multiple File Formats:
- Extend support for other document types such as DOCX, HTML, and TXT.

3. Improved Scalability:
- Use asynchronous processing for handling multiple users simultaneously.
- Implement load balancing for high-traffic environments.

4. Fine-Tuned Models:
- Integrate fine-tuned models for domain-specific use cases.

5. User Authentication:
- Add login functionality to track user activity and secure data.

### Acknowledgments
- Streamlit for enabling rapid development of web applications.
- LangChain and Sentence-Transformers for providing cutting-edge NLP models.
- Ollama for offering a private and efficient local LLM solution.
- Developers of open-source libraries used in this project.
