# operate.md

## Step1 环境准备
```powershell
# 进入项目根目录
cd E:\RAG_TCM_Diagnostic_Assistant
```

## Step2 安装依赖
```powershell
python -m venv .\.venv
. .\.venv\Scripts\Activate.ps1
pip install -r .\rag_app\requirements.txt
```

## Step3 构建向量库
```powershell
# 确保知识库文本在 rag_app/data/source/
python .\rag_app\ingest.py
```

## Step4 启动RAG问答
```powershell
python .\rag_app\query.py --query "输入你的问题"
```

## Step5 更换知识库流程（必须）
```powershell
# 1) 删除旧向量库
Remove-Item -Recurse -Force .\rag_app\vector_db

# 2) 放入新知识库
Copy-Item .\new_knowledge.txt .\rag_app\data\source\

# 3) 重新入库
python .\rag_app\ingest.py

# 4) 验证分块文件
Get-Item .\rag_app\data\chunks\chunks.json

# 5) 重新查询
python .\rag_app\query.py --query "你的新问题"
```
