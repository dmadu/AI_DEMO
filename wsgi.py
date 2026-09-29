import os
from dotenv import load

# Load environment variables from .env if present
from dotenv import load_dotenv
load_dotenv()

from src import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
