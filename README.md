# ⚙️ Elasticsearch ILM and Index Setup Automation

This Python script automates the setup of **Index Lifecycle Management (ILM)**, **index templates**, and **initial indices with aliases** in Elasticsearch.  
It’s perfect for teams managing production clusters that need **automatic rollover**, **lifecycle policies**, and **consistent mappings**.

---

## 🚀 Features
- Creates ILM policies (hot & warm phases)
- Defines index templates with mappings and lifecycle configuration
- Creates an initial write index and associates it with an alias
- Ensures repeatable and automated setup for large-scale indices

---

## 🧠 What It Does
1. **Creates an ILM Policy** (`prod_news_policy`)  
   Defines rollover at 20GB and sets shard priority.
2. **Creates an Index Template** (`prod_news_es_template`)  
   Applies custom mappings, shard/replica settings, and links to the ILM policy.
3. **Creates an Initial Index** (`prod_news_es-000001`)  
   Attaches alias `prod_news_es` and marks it as the write index.

---

## ⚙️ Requirements

- Python **3.8+**
- Elasticsearch **8.x+**
- `elasticsearch` Python client

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📘 Usage
1. Edit the Configuration
    In the script, update these variables:
```python
INDEX_NAME = "prod_news_es-000001"
ALIAS_NAME = "prod_news_es"
POLICY_NAME = "prod_news_policy"
TEMPLATE_NAME = "prod_news_es_template"
```
And your Elasticsearch connection details:
```python
es = Elasticsearch(
    "https://your-elastic-host",
    basic_auth=("elastic", "your-password")
)
```
2. Run the Script
```bash
python ilm_index_setup.py
```
3. Expected Output
```pgsql
ILM policy created successfully.
Index template created successfully.
Index 'prod_news_es-000001' created successfully with alias 'prod_news_es'.
```




