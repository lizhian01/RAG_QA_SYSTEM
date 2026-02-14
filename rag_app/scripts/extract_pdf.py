from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = ROOT / "docs" / "中医临床诊疗智能助手.pdf"
OUT_TXT = ROOT / "docs" / "中医临床诊疗智能助手.txt"
OUT_SOURCE = ROOT / "rag_app" / "data" / "source" / "中医临床诊疗智能助手.txt"


def main() -> None:
    OUT_TXT.parent.mkdir(parents=True, exist_ok=True)
    OUT_SOURCE.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open(PDF_PATH) as doc:
        all_text = []
        for i in range(doc.page_count):
            text = doc.load_page(i).get_text("text")
            all_text.append(f"\n\n=== Page {i+1} ===\n{text}")
    text = "".join(all_text)
    OUT_TXT.write_text(text, encoding="utf-8")
    OUT_SOURCE.write_text(text, encoding="utf-8")
    print(f"extracted to: {OUT_TXT}")
    print(f"copied to: {OUT_SOURCE}")


if __name__ == "__main__":
    main()
