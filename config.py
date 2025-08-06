import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBg--CpR8POpdXX3wFbsl8weIrVuajgpmo')

# Scraping Configuration
GOOGLE_NEWS_URL = "https://news.google.com/search?q=finance+business&hl=en-US&gl=US&ceid=US:en"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Clustering Configuration
K_CLUSTERS = 10
MAX_HEADLINES_PER_DAY = 200

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL = "models/gemini-pro"

# File paths
DATA_DIR = "data"
HEADLINES_FILE = os.path.join(DATA_DIR, "headlines.csv")
SUMMARIES_FILE = os.path.join(DATA_DIR, "summaries.csv")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True) 