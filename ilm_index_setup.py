from elasticsearch import Elasticsearch

# Constants
INDEX_NAME = "prod_news_es-000001" 
ALIAS_NAME = "prod_news_es"
POLICY_NAME = "prod_news_policy"
TEMPLATE_NAME = "prod_news_es_template"
SHARD_COUNT = 5
REPLICA_COUNT = 0

# Connect to Elasticsearch
es = Elasticsearch(
    "https://your-elastic-host",
    basic_auth=("elastic", "your-password"),
    request_timeout=60,
    max_retries=10,
    retry_on_timeout=True
)

# Step 1: Create ILM Policy

def create_ilm_policy():
    policy_body = {
        "phases": {
            "hot": {
                "actions": {
                    "rollover": {
                        "max_size": "20GB"
                    },
                    "set_priority": {
                        "priority": 100
                    }
                }
            },
            "warm": {
                "actions": {
                    "shrink": {
                        "number_of_shards": 1
                    },
                    "forcemerge": {
                        "max_num_segments": 1
                    },
                    "set_priority": {
                        "priority": 50
                    }
                }
            }
        }
    }
    es.ilm.put_lifecycle(name=POLICY_NAME, policy=policy_body)
    print("ILM policy created successfully.")

# Step 2: Create Index Template
def create_index_template():
    template_body = {
        "index_patterns": [f"{ALIAS_NAME}-*"],
        "template": {  # Corrected field name
            "settings": {
                "number_of_shards": SHARD_COUNT,
                "number_of_replicas": REPLICA_COUNT,
                "index.lifecycle.name": POLICY_NAME,
                "index.lifecycle.rollover_alias": ALIAS_NAME
                # "index.codec": "best_compression"  # Added compression setting
                # This setting tells Elasticsearch to use the best compression available for the index, which can help reduce the storage footprint,
                # especially for larger datasets. however, note that it may have a minor impact on indexing performance, but the trad-off is usally worthwhile when storage efficiency is a priority.
                
            },
            "mappings": {
                "properties": {
                    "author": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}
                    },
                    "author_cleaned": {
                        "properties": {
                            "author": {
                                "type": "text",
                                "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}
                            },
                            "author_id": {
                                "type": "text",
                                "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}
                            }
                        }
                    },
                    "author_url": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "categories": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "clean_html": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "content": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "createdAt": {"type": "date"},
                    "embedding_vector": {"type": "float"},
                    "entities": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "isProcessed": {"type": "boolean"},
                    "isScrapped": {"type": "boolean"},
                    "keywords": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "processedDate": {"type": "date"},
                    "processed_content": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "pubDate": {"type": "date"},
                    "rawHtml": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "retried": {"type": "boolean"},
                    "sentiment": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "sourceId": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "sourceName": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "stance": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "summary": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "summary_new": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "tfidf_vector": {"type": "float"},
                    "title": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}},
                    "updatedAt": {"type": "date"},
                    "url": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 2048}}}
                }
            }
        }
    }

    es.indices.put_index_template(name=TEMPLATE_NAME, body=template_body)
    print("Index template created successfully.")

# Step 3: Create Initial Index with Alias
def create_initial_index():
    if not es.indices.exists(index=INDEX_NAME):
        body = {
            "aliases": {
                ALIAS_NAME: {
                    "is_write_index": True
                }
            }
        }
        es.indices.create(index=INDEX_NAME, body=body)
        print(f"Index '{INDEX_NAME}' created successfully with alias '{ALIAS_NAME}'.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

# Run all steps
create_ilm_policy()
create_index_template()
create_initial_index()


