# ingestion/pdf_parser.py
import io
import os
from typing import Dict, Any, List
import pdfplumber
import fitz  # PyMuPDF

def parse_pdf(file_path: str) -> Dict[str, Any]:
    result = {
        "text": "",
        "tables": [],
        "images": []
    }

    # --- Extraction texte et tableaux (pdfplumber) ---
    with pdfplumber.open(file_path) as pdf:
        all_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)

            tables = page.extract_tables()
            for table in tables:
                csv_table = []
                for row in table:
                    csv_table.append(",".join(str(cell) if cell else "" for cell in row))
                result["tables"].append("\n".join(csv_table))

        result["text"] = "\n".join(all_text)

    # --- Extraction des images (PyMuPDF) ---
    doc = fitz.open(file_path)
    image_dir = os.path.join(os.path.dirname(file_path), "extracted_images")
    os.makedirs(image_dir, exist_ok=True)

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
            except fitz.fitz.FileDataError as err:
                # Erreur d'image corrompue
                print(f"[Warning] Impossible d'extraire l'image xref={xref}, page={page_index+1}. Raison : {err}")
                continue
            except Exception as e:
                # Catch-all pour éviter tout blocage
                print(f"[Error] Exception lors de l'extraction de l'image xref={xref}, page={page_index+1} : {e}")
                continue

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page{page_index+1}_img{img_index+1}.{image_ext}"
            image_path = os.path.join(image_dir, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            result["images"].append(image_path)

    doc.close()
    return result
