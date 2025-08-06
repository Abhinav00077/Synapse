import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os
from scraper import GoogleNewsScraper
from clustering import HeadlineClusterer
from summarizer import GeminiSummarizer
from scheduler import NewsScheduler
from config import DATA_DIR, HEADLINES_FILE, SUMMARIES_FILE

# Page configuration
st.set_page_config(
    page_title="News Headline Summarizer",
    page_icon="📰",
    layout="wide"
)

class SimpleNewsDashboard:
    def __init__(self):
        self.scraper = GoogleNewsScraper()
        self.clusterer = HeadlineClusterer()
        self.summarizer = GeminiSummarizer()
        self.scheduler = NewsScheduler()
    
    def load_data(self):
        """Load headlines and summaries data"""
        headlines = self.scraper.load_headlines()
        summaries = self.summarizer.load_summaries()
        return headlines, summaries
    
    def run_manual_pipeline(self):
        """Run the complete pipeline manually"""
        with st.spinner("Running news processing pipeline..."):
            try:
                # Scrape headlines
                headlines = self.scraper.scrape_headlines()
                if not headlines:
                    st.error("Failed to scrape headlines")
                    return False
                
                # Cluster headlines
                headline_texts = [h['headline'] for h in headlines]
                cluster_results = self.clusterer.cluster_headlines(headline_texts)
                cluster_summaries = self.clusterer.get_cluster_summaries(cluster_results)
                
                # Generate summaries
                summaries = self.summarizer.generate_all_summaries(cluster_summaries)
                
                if summaries:
                    # Save data
                    self.scraper.save_headlines(headlines)
                    self.summarizer.save_summaries(summaries)
                    self.clusterer.save_model()
                    
                    st.success(f"Pipeline completed! Generated {len(summaries)} summaries from {len(headlines)} headlines")
                    return True
                else:
                    st.error("Failed to generate summaries")
                    return False
                    
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                return False
    
    def display_metrics(self, headlines, summaries):
        """Display key metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Headlines", len(headlines))
        
        with col2:
            st.metric("Clusters", len(summaries))
        
        with col3:
            if headlines:
                latest_date = max([h['timestamp'] for h in headlines])
                st.metric("Latest Update", latest_date[:10])
        
        with col4:
            avg_headlines_per_cluster = len(headlines) / len(summaries) if summaries else 0
            st.metric("Avg/Cluster", f"{avg_headlines_per_cluster:.1f}")
    
    def display_cluster_summaries(self, summaries):
        """Display cluster summaries"""
        st.subheader("News Cluster Summaries")
        
        for i, summary in enumerate(summaries):
            with st.expander(f"Cluster {summary['cluster_id']} - {summary['headlines_count']} headlines"):
                st.write("**Summary:**")
                st.write(summary['summary'])
                st.write("**Headlines in this cluster:**")
                for headline in summary['headlines'][:5]:
                    st.write(f"• {headline}")
                if len(summary['headlines']) > 5:
                    st.write(f"... and {len(summary['headlines']) - 5} more headlines")
    
    def display_charts(self, headlines, summaries):
        """Display interactive charts"""
        st.subheader("📊 Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cluster size distribution
            if summaries:
                cluster_sizes = [s['headlines_count'] for s in summaries]
                fig = px.bar(
                    x=list(range(len(cluster_sizes))),
                    y=cluster_sizes,
                    title="Headlines per Cluster",
                    labels={'x': 'Cluster ID', 'y': 'Number of Headlines'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Timeline of headlines
            if headlines:
                df_headlines = pd.DataFrame(headlines)
                df_headlines['timestamp'] = pd.to_datetime(df_headlines['timestamp'])
                df_headlines['date'] = df_headlines['timestamp'].dt.date
                
                daily_counts = df_headlines.groupby('date').size().reset_index(name='count')
                fig = px.line(
                    daily_counts,
                    x='date',
                    y='count',
                    title="Daily Headlines Count",
                    labels={'date': 'Date', 'count': 'Number of Headlines'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def display_executive_summary(self):
        """Display executive summary if available"""
        st.subheader("🎯 Executive Summary")
        
        # Look for latest executive summary
        executive_files = [f for f in os.listdir(DATA_DIR) if f.startswith('executive_summary_')]
        if executive_files:
            latest_file = max(executive_files)
            with open(os.path.join(DATA_DIR, latest_file), 'r') as f:
                executive_data = json.load(f)
            
            st.write(f"**Latest Executive Summary ({latest_file[18:26]}):**")
            st.write(executive_data['executive_summary'])
        else:
            st.info("No executive summary available. Run the pipeline to generate one.")
    
    def run_dashboard(self):
        """Main dashboard function"""
        # Header
        st.title("News Headline Summarizer")
        st.markdown("### AI-Powered Financial News Analysis with Gemini API")
        
        # Sidebar
        st.sidebar.title("Controls")
        
        # Manual pipeline trigger
        if st.sidebar.button("🔄 Run Pipeline Now"):
            success = self.run_manual_pipeline()
            if success:
                st.rerun()
        
        # Data refresh
        if st.sidebar.button("🔄 Refresh Data"):
            st.rerun()
        
        st.sidebar.markdown("---")
        
        # Load data
        headlines, summaries = self.load_data()
        
        if not headlines and not summaries:
            st.warning("No data available. Run the pipeline to get started!")
            return
        
        # Display metrics
        self.display_metrics(headlines, summaries)
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["Summaries", "Analytics", "Executive Summary"])
        
        with tab1:
            if summaries:
                self.display_cluster_summaries(summaries)
            else:
                st.info("No summaries available. Run the pipeline to generate summaries.")
        
        with tab2:
            self.display_charts(headlines, summaries)
        
        with tab3:
            self.display_executive_summary()
        
        # Footer
        st.markdown("---")
        st.markdown("Built by Abhinav Pandey using BeautifulSoup, MiniLM, KMeans, Gemini API, and Streamlit")

def main():
    dashboard = SimpleNewsDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main() 