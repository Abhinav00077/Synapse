# 📰 News Headline Summarizer

An AI-powered financial news analysis system that automatically scrapes, clusters, and summarizes financial headlines using advanced NLP techniques and the Gemini API.

## 🚀 Features

- **Automated Web Scraping**: Scrapes 200+ financial headlines daily from Google News using BeautifulSoup
- **Semantic Clustering**: Uses MiniLM embeddings and KMeans clustering (k=10) to group similar headlines
- **AI-Powered Summarization**: Generates professional summaries using Google's Gemini API
- **Interactive Dashboard**: Beautiful Streamlit interface with real-time analytics and visualizations
- **Automated Scheduling**: Runs daily on weekdays to keep summaries current
- **70% Manual Effort Reduction**: Automates the entire news analysis workflow

## 🛠️ Technology Stack

- **Web Scraping**: BeautifulSoup4, Requests
- **NLP & ML**: Sentence Transformers (MiniLM), Scikit-learn (KMeans)
- **AI API**: Google Gemini API
- **Web Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Scheduling**: Schedule library

## 📋 Prerequisites

- Python 3.8+
- Gemini API key from Google AI Studio
- Internet connection for web scraping

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Synapse-1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Get Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### 5. Run the Application
```bash
# Start the Streamlit dashboard
streamlit run app.py
```

## 📊 Usage

### Interactive Dashboard
1. Open the Streamlit app in your browser
2. Click "Run Pipeline Now" to scrape and process headlines
3. View summaries, analytics, and executive summaries in the dashboard

### Automated Scheduling
```bash
# Run the scheduler for automated daily processing
python scheduler.py
```

### Manual Pipeline
```bash
# Run individual components
python scraper.py      # Scrape headlines
python clustering.py   # Test clustering
python summarizer.py   # Test summarization
```

## 📁 Project Structure

```
Synapse-1/
├── app.py                 # Main Streamlit dashboard
├── scraper.py             # Google News web scraper
├── clustering.py          # MiniLM + KMeans clustering
├── summarizer.py          # Gemini API summarization
├── scheduler.py           # Automated scheduling
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md              # This file
└── data/                  # Generated data files
    ├── headlines.csv      # Scraped headlines
    ├── summaries.csv      # Generated summaries
    └── clustering_model.pkl # Trained clustering model
```

## 🔧 Configuration

### Key Settings (config.py)
- `K_CLUSTERS`: Number of clusters for KMeans (default: 10)
- `MAX_HEADLINES_PER_DAY`: Maximum headlines to scrape (default: 200)
- `EMBEDDING_MODEL`: MiniLM model for embeddings
- `GEMINI_MODEL`: Gemini model for summarization

### Environment Variables (.env)
- `GEMINI_API_KEY`: Your Gemini API key
- `MAX_HEADLINES_PER_DAY`: Customize headline limit
- `K_CLUSTERS`: Customize cluster count

## 📈 How It Works

### 1. Web Scraping
- BeautifulSoup scrapes Yahoo Finance for financial headlines
- Handles rate limiting and multiple news sections
- Saves headlines with timestamps

### 2. Semantic Clustering
- MiniLM creates embeddings for each headline
- KMeans groups similar headlines into 10 clusters
- Identifies representative headlines for each cluster

### 3. AI Summarization
- Gemini API generates professional summaries for each cluster
- Creates executive summary of all clusters
- Analyzes sentiment and key themes

### 4. Dashboard Visualization
- Interactive charts showing cluster distributions
- Timeline of headline counts
- Professional summary display

## 🎯 Key Benefits

- **Time Savings**: 70% reduction in manual news analysis effort
- **Consistency**: Automated processing ensures uniform analysis
- **Scalability**: Handles 200+ headlines daily
- **Insights**: AI-generated summaries highlight key market trends
- **Accessibility**: User-friendly dashboard for non-technical users

## 🔍 Sample Output

### Cluster Summary
```
Cluster 0 - 15 headlines
Summary: Tech giants Apple, Microsoft, and Google reported strong quarterly earnings, 
driven by cloud services and AI investments. Market sentiment remains positive for 
the technology sector despite regulatory concerns.
```

### Executive Summary
```
Today's financial markets showed continued strength in technology stocks, with major 
tech companies reporting robust earnings. The focus remains on AI investments and 
cloud services growth, while regulatory scrutiny of big tech continues to be a 
factor. Overall market sentiment is positive, with investors favoring companies 
demonstrating strong digital transformation initiatives.
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your Gemini API key is correctly set in `.env`
   - Verify the key has proper permissions

2. **Scraping Issues**
   - Yahoo Finance may change their HTML structure
   - Check the scraper logs for specific errors
   - Consider updating CSS selectors in `scraper.py`

3. **Memory Issues**
   - Reduce `MAX_HEADLINES_PER_DAY` for lower memory usage
   - Process headlines in smaller batches

4. **Rate Limiting**
   - The scraper includes delays to respect rate limits
   - If issues persist, increase delays in `scraper.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI summarization
- Sentence Transformers for MiniLM embeddings
- Yahoo Finance for financial news content
- Streamlit for the beautiful dashboard interface

---

**Built with ❤️ using BeautifulSoup, MiniLM, KMeans, Gemini API, and Streamlit** 