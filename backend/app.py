from flask import Flask, jsonify
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "Welcome to the Flask Backend API"
    })

@app.route('/health')
def health():
    db_status = "disconnected"
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        conn.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "status": "healthy",
        "database": db_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
