from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import spacy
import datetime
import hashlib
import json
import yaml

# Load spaCy models
models = {
    "en": spacy.load("en_core_web_trf"),
    "fr": spacy.load("fr_core_news_sm")
}

# Load Elasticsearch config from YAML
def load_es_config(path="config.yml"):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config['elasticsearch']

# Initialize Elasticsearch client using config
es_config = load_es_config()
es_host = f"{es_config['url']}:{es_config['port']}"

if es_config.get('user') and es_config.get('password'):
    es = Elasticsearch(es_host, http_auth=(es_config['user'], es_config['password']))
else:
    es = Elasticsearch(es_host)

# Initialize Flask app
app = Flask(__name__)

# Log app startup
def log_startup():
    doc = {
        "event": "flask_app_started",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "message": "Flask app with spaCy started"
    }
    try:
        es.index(index="logs", body=doc)
        print("Startup log sent to Elasticsearch.")
    except Exception as e:
        print(f"Failed to log startup to Elasticsearch: {e}")
def log_process():
    doc = {
        "event": "tokens_add",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "message": "token added"
    }
    try:
        es.index(index="logs", body=doc)
        print("Startup log sent to Elasticsearch.")
    except Exception as e:
        print(f"Failed to log startup to Elasticsearch: {e}")



@app.route('/')
def get_info():
    return 'Spacy on Rest'

@app.route('/gettokens', methods=['POST'])
def process_string():
    data = request.json

    if not data or 'input_string' not in data or 'language' not in data:
        return jsonify({"error": "Please provide both 'input_string' and 'language' keys"}), 400

    input_string = data['input_string']
    language = data['language']

    if language not in models:
        return jsonify({"error": f"Unsupported language '{language}'. Supported: {list(models.keys())}"}), 400

    doc = models[language](input_string)
    table = []

    for token in doc:
        record = {
            "pos": token.pos_,
            "text": token.text,
            "dep": token.dep_,
            "lemma": token.lemma_,
            "tag": token.tag_,
            "shape": token.shape_,
            "sentence": input_string,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Compute SHA-256 hash for Elasticsearch ID
        record_str = json.dumps(record, sort_keys=True)
        uid = hashlib.sha256(record_str.encode('utf-8')).hexdigest()
        log_process()
        try:
            es.index(index="tokens", id=uid, body=record)
        except Exception as e:
            print(f"Failed to index token '{token.text}': {e}")



        table.append(record)

    return jsonify(table)

if __name__ == '__main__':
    log_startup()
    app.run(debug=True, port=81)
