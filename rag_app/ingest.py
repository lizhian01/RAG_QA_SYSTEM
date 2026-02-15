import json
import hashlib
from typing import List

import chromadb
from chromadb.config import Settings

from config import (
    EMBEDDING_MODEL,
    SOURCE_DIR,
    CHUNK_FILE,
    VECTOR_DB_DIR,
    get_client,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
from utils import iter_text_files, chunk_text

BATCH_SIZE = 64
COLLECTION_NAME = "tcm_rag"


def embed_texts(client, texts: List[str]) -> List[List[float]]:
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def main() -> None:
    if not SOURCE_DIR.exists():
        raise SystemExit(f"source dir not found: {SOURCE_DIR}")

    CHUNK_FILE.parent.mkdir(parents=True, exist_ok=True)
    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

    client = get_client()

    chroma = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR),
        settings=Settings(
            anonymized_telemetry=False,
            chroma_product_telemetry_impl="telemetry_noop.NoopTelemetry",
        ),
    )
    collection = chroma.get_or_create_collection(name=COLLECTION_NAME)

    try:
        if collection.count() > 0:
            collection.delete(where={})
    except Exception:
        pass

    chunk_records = []
    batch_texts, batch_ids, batch_metas = [], [], []
    total_chunks = 0

    for path in iter_text_files(SOURCE_DIR):
        text = path.read_text(encoding="utf-8")
        source_hash = hashlib.md5(str(path).encode("utf-8")).hexdigest()[:8]
        for idx, (chunk, start, end) in enumerate(
            chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
        ):
            chunk_id = f"{source_hash}-{idx:06d}"
            meta = {"source": str(path), "start": start, "end": end}
            chunk_records.append(
                {"id": chunk_id, "source": str(path), "start": start, "end": end, "text": chunk}
            )

            batch_texts.append(chunk)
            batch_ids.append(chunk_id)
            batch_metas.append(meta)
            total_chunks += 1

            if len(batch_texts) >= BATCH_SIZE:
                embeddings = embed_texts(client, batch_texts)
                collection.add(
                    ids=batch_ids,
                    documents=batch_texts,
                    embeddings=embeddings,
                    metadatas=batch_metas,
                )
                batch_texts, batch_ids, batch_metas = [], [], []

    if batch_texts:
        embeddings = embed_texts(client, batch_texts)
        collection.add(
            ids=batch_ids,
            documents=batch_texts,
            embeddings=embeddings,
            metadatas=batch_metas,
        )

    CHUNK_FILE.write_text(
        json.dumps(chunk_records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"chunks written: {CHUNK_FILE}")
    print(f"vector db path: {VECTOR_DB_DIR}")
    print(f"total chunks: {total_chunks}")


if __name__ == "__main__":
    main()
