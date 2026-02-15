# func.md

## 核心文件职责与调用关系

### `rag_app/config.py`
- 职责：读取 `secret.txt`、集中配置模型、路径、分块参数与上下文长度。
- 调用关系：被 `ingest.py`、`query.py` 引用。
- RAG位置：配置层。

### `rag_app/utils.py`
- 职责：文本清洗与分块（chunking）。
- 调用关系：`ingest.py` 调用。
- RAG位置：chunking。

### `rag_app/scripts/extract_pdf.py`
- 职责：将 `docs/` 下 PDF 提取为 TXT，并同步到 `rag_app/data/source/`。
- 调用关系：独立脚本。
- RAG位置：ingestion（文本准备）。

### `rag_app/ingest.py`
- 职责：读取 `data/source/*.txt`，分块、Embedding、写入 Chroma 向量库，生成 `chunks.json`。
- 调用关系：调用 `config.py`、`utils.py`、`telemetry_noop.py`。
- RAG位置：ingestion → chunking → embedding → indexing。

### `rag_app/query.py`
- 职责：向量检索并调用模型生成回答，支持 `top_k` 与 `max_context_chars`。
- 调用关系：调用 `config.py`、`prompts.py`、`telemetry_noop.py`。
- RAG位置：retrieval → generation。

### `rag_app/prompts.py`
- 职责：系统提示词与回答模板。
- 调用关系：`query.py` 调用。
- RAG位置：generation 提示层。

### `rag_app/telemetry_noop.py`
- 职责：关闭 Chroma telemetry 以避免报错。
- 调用关系：`ingest.py`、`query.py` 在创建 Client 时指定。
- RAG位置：基础设施适配。

### `rag_app/requirements.txt`
- 职责：依赖列表。
- 调用关系：安装依赖时使用。

### `rag_app/run.ps1`
- 职责：一键执行抽取、入库、查询。
- 调用关系：串联 `extract_pdf.py`、`ingest.py`、`query.py`。

### `secret.txt`
- 职责：保存 API Key（纯字符串）。
- 调用关系：`config.py` 读取。
- RAG位置：运行必需配置。

### `rag_app/data/source/`
- 职责：知识库文本输入目录，所有 `*.txt` 会被入库。
- 调用关系：`ingest.py` 读取。
- RAG位置：数据入口。

### `rag_app/vector_db/`
- 职责：向量库持久化目录。
- 调用关系：`ingest.py` 写入，`query.py` 读取。
- RAG位置：索引存储。

### `rag_app/data/chunks/chunks.json`
- 职责：记录分块结果，便于排查与追溯。
- 调用关系：`ingest.py` 生成。
- RAG位置：chunking 产物。
