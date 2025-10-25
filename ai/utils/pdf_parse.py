"""Utilities for extracting and cleaning text from PDF files."""

# utils/pdf_parse.py
import os
import re
import tempfile
import requests
from pypdf import PdfReader

# Precompiled regex to strip ASCII control chars except \t, \n, \r and also DEL (0x7F)
_CONTROL_CHARS_EXCEPT_NEWLINES = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+")
_ALL_CONTROL_CHARS = re.compile(r"[\x00-\x1F\x7F]+")


def _strip_control_chars(s: str, keep_newlines: bool = True) -> str:
    """Remove non-printable control characters from a string.

    - If keep_newlines is True (default), keeps tab (\t), newline (\n), and carriage return (\r)
      while removing the rest of C0 controls (0x00-0x1F) and DEL (0x7F).
    - If False, removes all those control characters including tabs/newlines.
    """
    if not s:
        return s
    pattern = _CONTROL_CHARS_EXCEPT_NEWLINES if keep_newlines else _ALL_CONTROL_CHARS
    return pattern.sub("", s)


def extract_text_from_pdf(file_url: str, *, clean: bool = True, keep_newlines: bool = True) -> str:
    """
    Extract text from a PDF file, given a local path or a URL.

    Args:
        file_url: Path to a local PDF file or an http(s) URL.
        clean: Whether to remove control characters from the extracted text. Default True.
        keep_newlines: When cleaning, keep \n/\r/\t. Default True.

    Returns:
        The concatenated text of all pages (optionally cleaned).
    """
    temp_path = None
    is_temp = False

    # If a URL is provided, download to a temporary file first, then parse
    if file_url.startswith(("http://", "https://")):
        try:
            with requests.get(file_url, timeout=20, stream=True) as response:
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive chunks
                            tmp.write(chunk)
                    temp_path = tmp.name
                    is_temp = True
        except requests.exceptions.RequestException as e:
            raise IOError(f"Failed to download PDF from URL: {file_url}") from e
    else:
        # Local file path
        if not os.path.exists(file_url):
            raise IOError(f"File not found at path: {file_url}")
        temp_path = file_url

    try:
        reader = PdfReader(temp_path)
        text_parts = []
        for page in reader.pages:
            # pypdf returns None for non-extractable pages
            txt = page.extract_text() or ""
            if clean:
                txt = _strip_control_chars(txt, keep_newlines=keep_newlines)
            text_parts.append(txt)
        return "".join(text_parts)
    finally:
        # Clean up temporary file if we created one
        if is_temp and temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                # Best-effort cleanup; ignore errors
                pass