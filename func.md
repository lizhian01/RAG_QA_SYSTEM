# func.md

## 每个文件作用
- `docs\中医临床诊疗智能助手.pdf`：核心资料，RAG 的唯一知识来源。
- `docs\中医临床诊疗智能助手.txt`：PDF 抽取后的纯文本。
- `secret.txt`：存放 API Key，仅包含 key 字符串。
- `rag_app\scripts\extract_pdf.py`：把 PDF 转为 TXT，并复制到 `rag_app\data\source\`。
- `rag_app\utils.py`：文本清洗与切分工具。
- `rag_app\config.py`：统一配置与读取 `secret.txt`。
- `rag_app\ingest.py`：切分文本、生成 `chunks.json`、写入 Chroma 向量库。
- `rag_app\prompts.py`：系统提示词与问答提示模板。
- `rag_app\query.py`：执行 RAG 检索并调用 `gpt-4o-mini` 生成回答。
- `rag_app\requirements.txt`：运行依赖。
- `rag_app\run.ps1`：一键执行（抽取 → 入库 → 查询）。
- `RAG_实战完整流程.md`：完整执行文档。

## 运行顺序
1. `rag_app\scripts\extract_pdf.py`
2. `rag_app\ingest.py`
3. `rag_app\query.py`
4. 或直接运行 `rag_app\run.ps1`

## 依赖说明
- `openai==1.40.0`
- `chromadb==0.5.5`
- `pymupdf==1.24.9`
