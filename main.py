from pathlib import Path

from src.excel_writer import write_rows
from src.llm.ollama_extractor import AadhaarData, extract_fields
from src.loader import load_files
from src.parser.image_parser import image_bytes
from src.parser.pdf_parser import render_pdf
from src.validator import validate

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "input"
OUTPUT_FILE = ROOT / "output" / "aadhaar_data.xlsx"
FIELDS = list(AadhaarData.model_fields)
HEADERS = ["File Name", *(f.title for f in AadhaarData.model_fields.values()), "Status", "Remarks"]


def main():
    files = load_files(INPUT_DIR)
    if not files:
        print(f"No PDF or JPEG files found in {INPUT_DIR}")
        return

    rows = []
    for file in files:
        print(f"Processing {file.name} ...")
        try:
            # Stage 1: convert the file to images
            images = render_pdf(file) if file.suffix.lower() == ".pdf" else [image_bytes(file)]
            # Stage 2: vision LLM extraction
            data = extract_fields(images)
        except Exception as e:
            rows.append([file.name, *[None] * len(FIELDS), "error", str(e)])
            print(f"  error: {e}")
            continue
        # Stage 3: validation
        issues = validate(data)
        values = data.model_dump()
        rows.append([file.name, *(values[f] for f in FIELDS), "review" if issues else "ok", "; ".join(issues)])
        print(f"  {'review: ' + '; '.join(issues) if issues else 'ok'}")

    # Stage 4: write to Excel
    write_rows(OUTPUT_FILE, HEADERS, rows)
    print(f"Saved {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
