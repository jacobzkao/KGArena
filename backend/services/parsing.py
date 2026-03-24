from __future__ import annotations

from io import BytesIO

from docx import Document
from pypdf import PdfReader


class UnsupportedFileTypeError(ValueError):
    pass


def parse_uploaded_file(filename: str, content: bytes) -> str:
    if filename.endswith('.txt'):
        return content.decode('utf-8', errors='ignore')
    if filename.endswith('.pdf'):
        return _parse_pdf(content)
    if filename.endswith('.docx'):
        return _parse_docx(content)
    raise UnsupportedFileTypeError('Unsupported file type. Please upload .txt, .pdf, or .docx')


def _parse_pdf(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    pages = [page.extract_text() or '' for page in reader.pages]
    return '\n'.join(pages).strip()


def _parse_docx(content: bytes) -> str:
    document = Document(BytesIO(content))
    return '\n'.join(paragraph.text for paragraph in document.paragraphs).strip()
