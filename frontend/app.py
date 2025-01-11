import streamlit as st
from utils.pdf_processor import PDFProcessor
from models.rag_model import RAGModel

def set_custom_style():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-image: linear-gradient(180deg, #2e7bcf 0%, #1a4c8c 100%);
            color: white;
        }
        
        .sidebar .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        .sidebar [data-testid="stFileUploader"] {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        
        .sidebar .sidebar-content h1 {
            color: white !important;
        }
        
        footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6;
            padding: 1rem;
            text-align: center;
            font-size: 0.8rem;
            border-top: 1px solid #e6e6e6;
        }
        
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            background-color: #f8f9fa;
        }
        
        /* Enhance header appearance */
        h1, h2, h3 {
            color: #1a4c8c;
            margin-bottom: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if 'rag_model' not in st.session_state:
        st.session_state.rag_model = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    if 'processor' not in st.session_state:
        st.session_state.processor = None

def display_chat_message(role, content):
    with st.chat_message(role):
        if isinstance(content, dict) and content.get('type') == 'image_response':
            st.write(f"Here are the images from page {content['page']}:")
            for idx, img in enumerate(content['images'], 1):
                st.image(img['image'], caption=f"Image {idx} from page {content['page']}")
        else:
            st.write(content)

def main():
    # Set page configuration
    st.set_page_config(
        page_title="PDF Q&A Chatbot",
        page_icon=":book:",
        layout="centered"
    )
    
    # Apply custom styling
    set_custom_style()
    initialize_session_state()

    # Sidebar for PDF upload and processing
    with st.sidebar:
        st.header("Upload PDF")
        pdf_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        if pdf_file:
            start_page = st.number_input("Start Page", min_value=1, value=1)
            end_page = st.number_input("End Page", min_value=start_page, value=start_page)
            
            if st.button("Process PDF", type="primary"):  
                with st.spinner("Processing PDF..."):
                    st.session_state.processor = PDFProcessor()
                    content = st.session_state.processor.extract_content(pdf_file, start_page, end_page)
                    
                    if content['success']:
                        st.session_state.rag_model = RAGModel()
                        st.session_state.rag_model.initialize_rag(
                            text_content=content['text'],
                            processor=st.session_state.processor
                        )
                        st.session_state.pdf_processed = True
                        st.success("PDF processed! Please ask questions in the chat.")
                    else:
                        st.error(content['message'])

    # Main chat interface
    st.header("PDF Q&A Chatbot")
    
    if not st.session_state.pdf_processed:
        st.info("Please upload and process a PDF first.")
        return

    # Display chat history
    for message in st.session_state.chat_history:
        display_chat_message(message["role"], message["content"])

    # Chat input
    if question := st.chat_input("Ask a question about your PDF"):
        display_chat_message("user", question)
        
        if st.session_state.rag_model:
            try:
                with st.spinner(""):
                    response = st.session_state.rag_model.get_response(question)
                    display_chat_message("assistant", response)
                    st.session_state.chat_history.extend([
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": response}
                    ])
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please process the PDF again.")
    
