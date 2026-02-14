import argparse
import chromadb
from chromadb.config import Settings

from config import EMBEDDING_MODEL, VECTOR_DB_DIR, CHAT_MODEL, get_client
from prompts import SYSTEM_PROMPT, QA_PROMPT_TEMPLATE

COLLECTION_NAME = "tcm_rag"


def build_prompt(contexts, query):
    context_str = "\n\n".join([f"[{i+1}] {c}" for i, c in enumerate(contexts)])
    return QA_PROMPT_TEMPLATE.format(context_str=context_str, query_str=query)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--top_k", type=int, default=5)
    args = parser.parse_args()

    client = get_client()

    chroma = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR),
        settings=Settings(anonymized_telemetry=False)
    )
    collection = chroma.get_collection(name=COLLECTION_NAME)

    q_embedding = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[args.query]
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=args.top_k
    )

    contexts = results["documents"][0] if results.get("documents") else []
    prompt = build_prompt(contexts, args.query)

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    answer = resp.choices[0].message.content

    print("=== Retrieved Contexts ===")
    for i, c in enumerate(contexts, 1):
        print(f"[{i}] {c}\n")
    print("=== Answer ===")
    print(answer)


if __name__ == "__main__":
    main()
