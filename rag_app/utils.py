from pathlib import Path
from typing import Iterable, Iterator, Tuple


def iter_text_files(source_dir: Path) -> Iterable[Path]:
    return sorted(source_dir.rglob("*.txt"))


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 200,
) -> Iterator[Tuple[str, int, int]]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    text = normalize_text(text)
    start = 0
    total = len(text)
    while start < total:
        end = min(total, start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            yield chunk, start, end
        start = end - overlap
        if start < 0:
            start = 0
        if start >= total:
            break
