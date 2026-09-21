from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Path to the PDF or DOCX file to convert")
) -> str:
    """Convert a PDF or DOCX file to markdown.

    Reads a document file from the given path and converts its contents
    to markdown-formatted text. Supports PDF and DOCX formats.

    When to use:
    - When you have a local PDF or DOCX file and need its contents as markdown
    - When you want to extract text from a document for further processing
    - When integrating document conversion into workflows

    When not to use:
    - For formats other than PDF and DOCX
    - For very large files (conversion happens in memory)

    Examples:
    >>> document_path_to_markdown("/path/to/document.pdf")
    # PDF Title\n\nPDF content here...
    >>> document_path_to_markdown("/path/to/report.docx")
    # Report Header\n\nReport content...
    """
    path = Path(file_path)

    # Extract and validate file extension first
    extension = path.suffix.lstrip(".").lower()
    if extension not in ("pdf", "docx"):
        raise ValueError(
            f"Unsupported file format: {extension}. Supported formats are: pdf, docx"
        )

    # Validate file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read file as binary
    with open(path, "rb") as f:
        binary_data = f.read()

    # Convert using existing function
    return binary_document_to_markdown(binary_data, extension)
