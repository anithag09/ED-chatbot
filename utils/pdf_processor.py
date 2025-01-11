import fitz
import io
from PIL import Image

class PDFProcessor:
    def __init__(self):
        self.text_content = []
        self.images = []
        self.current_page_range = None
        
    def extract_content(self, pdf_file, start_page, end_page):
        try:
            self.current_page_range = (start_page, end_page)
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            
            max_pages = doc.page_count
            start_page = max(1, min(start_page, max_pages))
            end_page = max(start_page, min(end_page, max_pages))
            
            for page_num in range(start_page-1, end_page):
                page = doc[page_num]
                
                # Text extraction
                text = page.get_text("text")  # Get raw text first
                
                # Process text blocks with metadata
                blocks = page.get_text("dict")["blocks"]
                structured_text = []
                
                for block in blocks:
                    if block.get("type") == 0:  # Text block
                        block_text = ""
                        for line in block.get("lines", []):
                            line_text = []
                            for span in line.get("spans", []):
                                # Preserve font information and styling
                                text = span.get("text", "").strip()
                                if text:
                                    line_text.append(text)
                            if line_text:
                                block_text += " ".join(line_text) + "\n"
                        if block_text:
                            structured_text.append(block_text)
                
                # Combine both approaches for comprehensive text capture
                final_text = "\n".join(structured_text) if structured_text else text
                
                self.text_content.append({
                    'page': page_num + 1,
                    'content': final_text,
                    'metadata': {
                        'page_number': page_num + 1,
                        'has_images': bool(page.get_images())
                    }
                })
                # Image extraction
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    self.images.append({
                        'page': page_num + 1,
                        'image': image,
                        'index': img_index
                    })
            
            # Create a consolidated text version for better context
            consolidated_text = "\n\n".join([item['content'] for item in self.text_content])
            
            return {
                'text': self.text_content,
                'consolidated_text': consolidated_text,  # Added for better QA
                'images': self.images,
                'success': True,
                'message': f'Successfully extracted content from pages {start_page} to {end_page}'
            }
            
        except Exception as e:
            return {
                'text': [],
                'images': [],
                'success': False,
                'message': f'Error processing PDF: {str(e)}'
            }
