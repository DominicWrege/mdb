#!/bin/sh


# $1 nach topic name

curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
    "name": "elasticsearch-sink-rising-posts",
    "config": {
        "connector.class":"io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
        "tasks.max": "1",
        "topics":"rising_posts",
        "key.converter":"org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable":"false",
        "value.converter":"org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable":"false","key.ignore": "true",
        "schema.ignore":"true",
        "connection.url": "http://172.22.160.87:9200",
        "type.name": "_doc",
        "name": "elasticsearch-sink-rising-posts"
    }
}' | jq
