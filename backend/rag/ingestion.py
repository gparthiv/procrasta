import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

from rag.resources import vector_store, api_key
from services.document_parser import (
    parse_pdf,
    parse_pptx,
    ocr_image_with_gemini,
)


client = genai.Client(
    api_key=api_key
)


def process_upload(
    file_path: str,
    filename: str,
    user_id: str,
):

    ext = os.path.splitext(filename)[1].lower()

    extracted_docs = []

    try:

        if ext == ".pdf":

            extracted_docs = parse_pdf(
                file_path,
                filename,
            )

        elif ext == ".pptx":

            extracted_docs = parse_pptx(
                file_path,
                filename,
            )

        elif ext in [".png", ".jpg", ".jpeg"]:

            extracted_docs = ocr_image_with_gemini(
                file_path,
                filename,
                client,
            )

        else:

            raise ValueError(
                "Unsupported file format."
            )

        extracted_docs = [
            doc
            for doc in extracted_docs
            if doc.page_content
            and doc.page_content.strip()
        ]

        if not extracted_docs:
            raise ValueError(
                "Could not extract any text from the file."
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = splitter.split_documents(
            extracted_docs
        )

        chunks = [
            chunk
            for chunk in chunks
            if chunk.page_content
            and chunk.page_content.strip()
        ]

        if not chunks:
            raise ValueError(
                "No usable text was found after chunking."
            )
        for chunk in chunks:
          chunk.metadata["user_id"] = user_id
          
        vector_store.add_documents(chunks)

        return {
            "status": "success",
            "filename": filename,
            "documents_extracted": len(extracted_docs),
            "chunks_created": len(chunks),
        }

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)