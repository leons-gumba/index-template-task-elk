# CRUD operations to test in DevTools

# GET /_cat/indices/container

# GET /_index_template/container-template

# GET /_data_stream/container-test-resource

# DELETE /container

# DELETE /_index_template/container-template

# DELETE /container-test-resource

# GET /_data_stream

# POST container-test-resource/_doc/test-document-one
# {
# "@timestamp": "YYYY-MM-DD",
# "message": "This is a test message"
# }

# GET container-test-resource/_doc/test-document-one

# Import Elasticsearch library
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
client = Elasticsearch(
    hosts=["https://my-deployment-f7c97c.es.westeurope.azure.elastic-cloud.com:9243"],
    basic_auth=("elastic", "X1pw1F2mJdry3VWHfmzMwMEl")
)

# Index
index_name = "container"

# Check if the index exists
if not client.indices.exists(index=index_name):
    # Create the index if it doesn't exist
    client.indices.create(index=index_name)

# Delete the existing index template if it exists
index_template_name = f"{index_name}-template"
if client.indices.exists_template(name=index_template_name):
    client.indices.delete_template(name=index_template_name)

# Index template
index_template = {
    "index_patterns": [f"{index_name}-*"],
    "template": {
        "settings": {
            "index.number_of_shards": 1,
            "index.number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "labels": {
                    "properties": {
                        "stratosphere-cluster-name": {"type": "keyword"},
                        "stratosphere-geography-name": {"type": "keyword"},
                        "stratosphere-plane-type": {"type": "keyword"},
                        "stratosphere-project-name": {"type": "keyword"},
                        "stratosphere-resource-name": {"type": "keyword"},
                        "stratosphere-stage-name": {"type": "keyword"},
                        "kubernetes-container-name": {"type": "keyword"}
                    }
                }
            }
        }
    },
    "priority": 10  # Specify a higher priority for the new index template
}

# Create the index template
client.indices.put_index_template(
    name=index_template_name,
    body=index_template
)

# Assign resource type
resource_type = "test-resource"

# Delete the existing data stream template if it exists
data_stream_template_name = f"{index_name}-{resource_type}-template"
if client.indices.exists_template(name=data_stream_template_name):
    client.indices.delete_template(name=data_stream_template_name)

# Data stream template
data_stream_template = {
    "index_patterns": [f"{index_name}-{resource_type}-*"],
    "data_stream": {},
    "template": {
        "settings": {
            "index.number_of_shards": 1,
            "index.number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "timestamp": {
                    "type": "date"
                }
            }
        }
    }
}

# Create or update the data stream template
client.indices.put_index_template(
    name=data_stream_template_name,
    body=data_stream_template
)

# Create the data stream index
data_stream_index = f"{index_name}-{resource_type}"
client.indices.create(
    index=data_stream_index
)
