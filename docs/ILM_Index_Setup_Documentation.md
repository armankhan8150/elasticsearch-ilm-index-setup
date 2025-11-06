# 🧾 Elasticsearch ILM Index Setup Script Documentation

## **Overview**
This Python script automates the setup of an Elasticsearch index with **Index Lifecycle Management (ILM)**, an **index template**, and an **initial write index with alias**.  
It is designed to support efficient storage, rollover, and lifecycle management for large-scale news datasets (e.g., News Analyzer data).

---

## **Key Features**
- **Automates ILM policy creation** for rollover and optimization.  
- **Defines index template** with mappings and settings for text, date, boolean, and numeric fields.  
- **Creates initial index with alias** for seamless rollover and indexing continuity.  
- **Supports scalability** with configurable shard and replica counts.  

---

## **Constants**
| Constant | Description |
|-----------|-------------|
| `INDEX_NAME` | The name of the initial physical index (e.g., `prod_news_es-000001`). |
| `ALIAS_NAME` | The alias for the index (e.g., `prod_news_es`). Used for rollover. |
| `POLICY_NAME` | The name of the ILM policy to be created (e.g., `prod_news_policy`). |
| `TEMPLATE_NAME` | The name of the index template (e.g., `prod_news_es_template`). |
| `SHARD_COUNT` | Number of primary shards for the index. |
| `REPLICA_COUNT` | Number of replica shards for redundancy. |

---

## **1. Connect to Elasticsearch**
```python
es = Elasticsearch(
    "https://your-elastic-host",
    basic_auth=("elastic", "your-password"),
    request_timeout=60,
    max_retries=10,
    retry_on_timeout=True
)
```

This creates a resilient connection to your Elasticsearch cluster with automatic retries and timeouts.

---

## **2. Create ILM Policy**
### Function: `create_ilm_policy()`

**Purpose:**  
Defines a lifecycle policy to automatically manage index rollover and optimization phases.

**Phases Defined:**

| Phase | Actions | Description |
|--------|----------|-------------|
| **Hot Phase** | - Rollover at 20GB<br>- Set index priority to 100 | Used for active indexing and fresh data. |
| **Warm Phase** | - Shrink to 1 shard<br>- Force merge to 1 segment<br>- Lower priority to 50 | Used for less-frequently queried data to save resources. |

**Example:**
```python
create_ilm_policy()
```

**Output:**
```
ILM policy created successfully.
```

---

## **3. Create Index Template**
### Function: `create_index_template()`

**Purpose:**  
Defines the structure (mappings and settings) applied to all indices matching the alias pattern.

**Template Includes:**
- **Index pattern:** `prod_news_es-*`
- **Lifecycle policy linkage:** Connects the index to the ILM policy.
- **Mappings:** Defines field types for various properties (text, keyword, date, float, boolean, etc.).
- **Settings:**
  - Configurable shard and replica counts.
  - Lifecycle alias and policy references.
  - Optional compression (commented in script).

**Example:**
```python
create_index_template()
```

**Output:**
```
Index template created successfully.
```

---

## **4. Create Initial Index with Alias**
### Function: `create_initial_index()`

**Purpose:**  
Creates the first physical index (e.g., `prod_news_es-000001`) and associates it with the alias (`prod_news_es`).  
This alias will serve as the *write index* and future rollover target.

**Logic:**
- Checks if the index already exists.
- If not, creates it with the alias marked as `is_write_index=True`.

**Example:**
```python
create_initial_index()
```

**Output:**
```
Index 'prod_news_es-000001' created successfully with alias 'prod_news_es'.
```

---

## **5. Execution Flow**
The script executes all three setup steps in sequence:
```python
create_ilm_policy()
create_index_template()
create_initial_index()
```

After successful execution, your Elasticsearch cluster will have:
1. A lifecycle policy (`prod_news_policy`)
2. A reusable index template (`prod_news_es_template`)
3. An initialized index (`prod_news_es-000001`)
4. A rollover alias (`prod_news_es`)

---

## **Rollover Example (Manual Trigger)**
Once the index exceeds the `max_size` defined in the ILM policy, Elasticsearch will **automatically** roll over to a new index (e.g., `prod_news_es-000002`).

You can also manually trigger rollover if needed:
```bash
POST /prod_news_es/_rollover
```

---

## **Error Handling**
- The script checks if the index already exists to avoid duplicate creation.
- Retries and timeouts are configured for reliable connectivity.

---

## **Customization Notes**
- Adjust `max_size` in ILM policy as per your dataset size.
- Modify `SHARD_COUNT` and `REPLICA_COUNT` based on cluster size.
- Uncomment `"index.codec": "best_compression"` for storage optimization.
- Extend mappings to include additional fields as your schema evolves.

---

## **Example Usage**
```bash
python ilm_index_setup.py
```

**Expected Output:**
```
ILM policy created successfully.
Index template created successfully.
Index 'prod_news_es-000001' created successfully with alias 'prod_news_es'.
```

---

## **References**
- [Elasticsearch ILM Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)  
- [Elasticsearch Index Templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html)  
- [Elasticsearch Python Client](https://elasticsearch-py.readthedocs.io/en/latest/)