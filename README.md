# 一、项目简介

- 项目名称：基于RAG的知识库问答系统
- 项目简介：对本地知识库进行切分、向量化与检索，基于检索证据生成回答，支持快速替换知识库与可复现查询流程。
- 使用 gpt-4o-mini + gptsapi
- 输入支持 PDF / TXT
- 工程流水线：ingestion → chunking → embedding → indexing → retrieval → generation

---

# 二、功能概览

- 本地知识库入库（`rag_app/data/source/*.txt`）
- PDF 转 TXT（`rag_app/scripts/extract_pdf.py`）
- 向量库持久化（Chroma）
- 检索 + 生成回答（gpt-4o-mini）
- 可控分块与上下文长度

---

# 三、项目目录结构说明

```text
E:\RAG_TCM_Diagnostic_Assistant
├─ README.md
├─ func.md
├─ operate.md
├─ secret.txt
├─ docs
├─ rag_app
│  ├─ config.py
│  ├─ utils.py
│  ├─ ingest.py
│  ├─ query.py
│  ├─ prompts.py
│  ├─ telemetry_noop.py
│  ├─ requirements.txt
│  ├─ run.ps1
│  ├─ data
│  │  ├─ source
│  │  │  └─ knowledge.txt
│  │  └─ chunks
│  │     └─ chunks.json
│  ├─ vector_db
│  ├─ logs
│  └─ scripts
│     └─ extract_pdf.py
```

---

# 四、RAG工作流程（核心）

1. **准备知识库**
   - TXT 放入 `rag_app/data/source/`
   - 或 PDF 放入 `docs/`
   ```powershell
   Copy-Item .\rag_app\data\source\knowledge.txt .\rag_app\data\source\
   ```

2. **PDF 提取（可选）**
   - PDF 位置：`docs/`
   - 输出：`docs/*.txt` 同步到 `rag_app/data/source/`
   ```powershell
   python .\rag_app\scripts\extract_pdf.py
   ```

3. **入库（ingest → chunk → embedding → indexing）**
   ```powershell
   python .\rag_app\ingest.py
   ```

4. **检索与生成（retrieve → generate）**
   ```powershell
   python .\rag_app\query.py --query "你的问题"
   ```

---

# 五、环境配置与API说明

- `secret.txt` 写入 API Key
- 读取方式：
  ```python
  def load_api_key():
      with open("secret.txt","r",encoding="utf-8") as f:
          return f.read().strip()

  API_KEY = load_api_key()

  client = OpenAI(
      api_key=API_KEY,
      base_url="https://api2.gptsapi.net/v1"
  )
  ```
- 模型：`gpt-4o-mini`

---

# 六、快速开始（完整运行流程）

```powershell
# 1) 创建环境并安装依赖
python -m venv .\.venv
. .\.venv\Scripts\Activate.ps1
pip install -r .\rag_app\requirements.txt

# 2) 入库
python .\rag_app\ingest.py

# 3) 查询
python .\rag_app\query.py --query "你的问题"
```

---

# 七、示例命令

```powershell
# 自定义召回数量与上下文长度
python .\rag_app\query.py --query "你的问题" --top_k 3 --max_context_chars 1200

# 使用一键脚本
powershell -ExecutionPolicy Bypass -File .\rag_app\run.ps1
```

---

# 八、如何替换知识库

1. 删除旧向量库
   ```powershell
   Remove-Item -Recurse -Force .\rag_app\vector_db
   ```
2. 将新知识库放入 `rag_app/data/source/`
   ```powershell
   Copy-Item .\new_knowledge.txt .\rag_app\data\source\
   ```
3. 重新运行 `ingest.py`
   ```powershell
   python .\rag_app\ingest.py
   ```
4. 验证 `chunks.json` 是否生成
   ```powershell
   Get-Item .\rag_app\data\chunks\chunks.json
   ```
5. 重新执行 `query.py`
   ```powershell
   python .\rag_app\query.py --query "你的新问题"
   ```

原因：向量库保存的是旧知识文本的向量索引，不重建会导致检索命中旧内容。
