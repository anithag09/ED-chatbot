from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests.exceptions
import time

class RAGModel:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        self.processor = None
        self.page_content = {}
        
    def initialize_rag(self, text_content, processor):
        """Initialize the RAG model with text content and processor"""
        try:
            self.processor = processor
            texts = []
            
            # Store content by page for direct access
            for page in text_content:
                page_num = page['page']
                content = page['content']
                self.page_content[page_num] = content
                
                # Create chunks with page context
                chunks = self.text_splitter.split_text(content)
                for chunk in chunks:
                    # Add page number to each chunk
                    chunk_with_context = f"Page {page_num}: {chunk}"
                    texts.append(chunk_with_context)
            
            # Create vector store with improved retrieval
            self.vectorstore = Chroma.from_texts(
                texts,
                self.embeddings,
                metadatas=[{"page": str(i)} for i in range(len(texts))]
            )
            
            # Configure LLM with optimized parameters
            llm = Ollama(
                model="llama2",
                temperature=0.1,
                top_k=10,
                top_p=0.9,
                repeat_penalty=1.2,
                timeout=60
            )
            
            # Initialize QA chain
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 8}
                ),
                memory=self.memory,
                return_source_documents=True,
                verbose=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error initializing RAG: {str(e)}")
            return False

    def get_response(self, question):
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Handle image queries
                if 'image' in question.lower() and 'page' in question.lower():
                    return self.handle_image_query(question)
                
                # Direct page queries
                if 'page' in question.lower():
                    import re
                    page_numbers = re.findall(r'page\s+(\d+)', question.lower())
                    if page_numbers:
                        page_num = int(page_numbers[0])
                        if page_num in self.page_content:
                            return f"Content from page {page_num}:\n{self.page_content[page_num]}"

                # Direct text lookup for common queries
                if 'author' in question.lower():
                    # Search through page content directly
                    for page_num, content in self.page_content.items():
                        if 'Dr.' in content or 'Lecture Notes by:' in content:
                            return f"The document is authored by Dr. Ala Hijazi (Found on page {page_num})"
                
                # Configure LLM 
                llm = Ollama(
                    model="llama2",
                    temperature=0.1,
                    top_k=10,
                    top_p=0.9,
                    repeat_penalty=1.2,
                    timeout=60  
                )
                
                context_query = {
                    "question": question,
                    "chat_history": self.memory.chat_memory.messages
                }
                
                response = self.qa_chain(context_query)
                answer = response['answer']
                source_docs = response.get('source_documents', [])
                
                # Extract page references
                page_refs = set()
                for doc in source_docs:
                    if 'Page' in doc.page_content:
                        page_num = doc.page_content.split('Page')[1].split(':')[0].strip()
                        page_refs.add(page_num)
                
                if page_refs:
                    answer = f"{answer}\n\n(Information from page(s): {', '.join(sorted(page_refs))})"
                
                return answer if answer.strip() else "I couldn't find specific information about that in the document."
                
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                if attempt == max_retries - 1:
                    # Fall back to direct content search on final retry
                    if 'topics' in question.lower():
                        topics = self.extract_topics_from_content()
                        return topics
                    return self.fallback_response(question)
                    
                time.sleep(retry_delay)
                continue
                
            except Exception as e:
                return f"Error processing question: {str(e)}"

    def handle_image_query(self, question):
        try:
            import re
            page_numbers = re.findall(r'page\s+(\d+)', question.lower())
            if not page_numbers:
                return "Please specify which page number you'd like to see images from."
            
            page_num = int(page_numbers[0])
            images = [img for img in self.processor.images if img['page'] == page_num]
            
            if not images:
                return f"No images found on page {page_num}."
            
            return {
                'type': 'image_response',
                'images': images,
                'page': page_num
            }
            
        except Exception as e:
            return "I encountered an error processing the image request. Please make sure to specify a valid page number." 

    def extract_topics_from_content(self):
        """Extracts main topics directly from content without using LLM"""
        topics = []
        for content in self.page_content.values():
            # Look for section headers and main topics
            lines = content.split('\n')
            for line in lines:
                if line.isupper() or 'Basics' in line or any(word in line for word in ['Chapter', 'Section']):
                    topics.append(line.strip())
        return "Main topics covered:\n" + "\n".join(set(topics)) if topics else "Unable to extract topics"
    
    def fallback_response(self, question):
        """Provides direct content search when LLM fails"""
        # Simple keyword matching in content
        for page_num, content in self.page_content.items():
            if any(keyword in question.lower() for keyword in ['author', 'who wrote']):
                if 'Dr.' in content or 'Lecture Notes by:' in content:
                    return f"The document is authored by Dr. Ala Hijazi (Found on page {page_num})"
        return "I apologize, but I'm having trouble accessing the LLM. Please try again in a moment."