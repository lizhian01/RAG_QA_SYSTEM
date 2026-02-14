# 一、项目目标
1. 基于 `中医临床诊疗智能助手.pdf` 构建可运行的 RAG 问答项目。
2. 完成抽取、切分、向量化、检索与回答生成流程。
3. 统一使用 OpenAI Compatible API（`https://api2.gptsapi.net/v1` + `gpt-4o-mini`）。

# 二、项目目录结构
```text
E:\RAG_TCM_Diagnostic_Assistant
├─ docs
│  ├─ 中医临床诊疗智能助手.pdf
│  └─ 中医临床诊疗智能助手.txt
├─ rag_app
│  ├─ config.py
│  ├─ utils.py
│  ├─ ingest.py
│  ├─ query.py
│  ├─ prompts.py
│  ├─ requirements.txt
│  ├─ run.ps1
│  ├─ data
│  │  ├─ source
│  │  └─ chunks
│  │     └─ chunks.json
│  ├─ vector_db
│  ├─ logs
│  └─ scripts
│     └─ extract_pdf.py
└─ RAG_实战完整流程.md
```

# 三、完整执行流程
## Step 1：填写 API KEY
- 文件路径：`E:\RAG_TCM_Diagnostic_Assistant\rag_app\config.py`
- 操作：把以下变量改成你的 key。
```python
# ===== 在这里填写你的 gptsapi key =====
API_KEY = "sk-y0Wf126e0a04505b6dd942fb3bf726622f3403d3de89POla"
```

## Step 2：创建虚拟环境并安装依赖
- 代码块：
```powershell
# run in: E:\RAG_TCM_Diagnostic_Assistant
python -m venv E:\RAG_TCM_Diagnostic_Assistant\.venv
. E:\RAG_TCM_Diagnostic_Assistant\.venv\Scripts\Activate.ps1
pip install -r E:\RAG_TCM_Diagnostic_Assistant\rag_app\requirements.txt
```

## Step 3：切分 + 向量化 + 入库
- 代码块：
```powershell
# run in: E:\RAG_TCM_Diagnostic_Assistant
python E:\RAG_TCM_Diagnostic_Assistant\rag_app\ingest.py
```

## Step 4：检索并生成回答
- 代码块：
```powershell
# run in: E:\RAG_TCM_Diagnostic_Assistant
python E:\RAG_TCM_Diagnostic_Assistant\rag_app\query.py --query "肾阳虚有什么表现？"
```

# 四、最终一键运行方式
```powershell
# run in: E:\RAG_TCM_Diagnostic_Assistant
powershell -ExecutionPolicy Bypass -File E:\RAG_TCM_Diagnostic_Assistant\rag_app\run.ps1
```
