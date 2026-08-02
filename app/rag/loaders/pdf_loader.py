import os
import logging

logger = logging.getLogger("agentflow.rag.loaders.pdf_loader")

class PDFLoader:
    """
    Loader for PDF files. Uses pypdf if available, otherwise falls back to a placeholder.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> str:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        try:
            import pypdf
            logger.info(f"Extracting PDF text using pypdf: {self.file_path}")
            reader = pypdf.PdfReader(self.file_path)
            text_parts = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n\n".join(text_parts)
        except ImportError:
            logger.warning("pypdf is not installed. To parse PDFs, install it with 'pip install pypdf'. Falling back to metadata readout.")
            # Basic fallback: read raw bytes or return placeholder
            basename = os.path.basename(self.file_path)
            return f"[PDF Placeholder] Content of PDF file: {basename}. (Please install pypdf to parse actual PDF contents)."
