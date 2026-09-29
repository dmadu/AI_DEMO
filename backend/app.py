import os
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    db_status = "disconnected"
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB", "appdb"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
            host=os.environ.get("POSTGRES_HOST", "database"),
            port=os.environ.get("POSTGRES_PORT", "5432")
        )
        conn.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "status": "healthy",
        "database": db_status
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Flask Backend API"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
