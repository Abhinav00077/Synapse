import schedule
import time
import logging
from datetime import datetime
import os
from scraper import GoogleNewsScraper
from clustering import HeadlineClusterer
from summarizer import GeminiSummarizer
from config import DATA_DIR

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(DATA_DIR, 'scheduler.log')),
        logging.StreamHandler()
    ]
)

class NewsScheduler:
    def __init__(self):
        self.scraper = GoogleNewsScraper()
        self.clusterer = HeadlineClusterer()
        self.summarizer = GeminiSummarizer()
        
    def run_daily_pipeline(self):
        """
        Run the complete news processing pipeline
        """
        try:
            logging.info("Starting daily news processing pipeline...")
            
            # Step 1: Scrape headlines
            logging.info("Step 1: Scraping headlines from Google News...")
            headlines = self.scraper.scrape_headlines()
            
            if not headlines:
                logging.error("No headlines scraped. Pipeline stopped.")
                return
            
            logging.info(f"Successfully scraped {len(headlines)} headlines")
            
            # Step 2: Cluster headlines
            logging.info("Step 2: Clustering headlines...")
            headline_texts = [h['headline'] for h in headlines]
            cluster_results = self.clusterer.cluster_headlines(headline_texts)
            cluster_summaries = self.clusterer.get_cluster_summaries(cluster_results)
            
            logging.info(f"Created {len(cluster_summaries)} clusters")
            
            # Step 3: Generate summaries
            logging.info("Step 3: Generating summaries...")
            summaries = self.summarizer.generate_all_summaries(cluster_summaries)
            
            if summaries:
                logging.info(f"Generated {len(summaries)} summaries")
                
                # Step 4: Generate executive summary
                logging.info("Step 4: Generating executive summary...")
                executive_summary = self.summarizer.generate_executive_summary(summaries)
                
                # Step 5: Save results
                logging.info("Step 5: Saving results...")
                self.scraper.save_headlines(headlines)
                self.summarizer.save_summaries(summaries)
                self.clusterer.save_model()
                
                # Save executive summary
                if executive_summary:
                    executive_file = os.path.join(DATA_DIR, f"executive_summary_{datetime.now().strftime('%Y%m%d')}.json")
                    import json
                    with open(executive_file, 'w') as f:
                        json.dump(executive_summary, f, indent=2)
                    logging.info(f"Executive summary saved to {executive_file}")
                
                logging.info("Daily pipeline completed successfully!")
                
            else:
                logging.error("No summaries generated. Pipeline failed.")
                
        except Exception as e:
            logging.error(f"Error in daily pipeline: {e}")
    
    def run_test_pipeline(self):
        """
        Run a test pipeline with sample data
        """
        logging.info("Running test pipeline...")
        
        # Sample headlines for testing
        test_headlines = [
            "Apple stock rises on strong iPhone sales",
            "Tesla reports record quarterly earnings",
            "Microsoft announces new AI features",
            "Google parent Alphabet beats revenue expectations",
            "Amazon expands cloud services",
            "Facebook parent Meta faces regulatory scrutiny",
            "Netflix subscriber growth slows",
            "Disney streaming service gains momentum",
            "Intel chip shortage affects production",
            "AMD gains market share in processors"
        ]
        
        try:
            # Test clustering
            cluster_results = self.clusterer.cluster_headlines(test_headlines)
            cluster_summaries = self.clusterer.get_cluster_summaries(cluster_results)
            
            # Test summarization
            summaries = self.summarizer.generate_all_summaries(cluster_summaries)
            
            logging.info(f"Test pipeline completed. Generated {len(summaries)} summaries.")
            
        except Exception as e:
            logging.error(f"Error in test pipeline: {e}")
    
    def schedule_daily_run(self, time_str="09:00"):
        """
        Schedule the daily pipeline to run at a specific time
        """
        schedule.every().day.at(time_str).do(self.run_daily_pipeline)
        logging.info(f"Scheduled daily pipeline to run at {time_str}")
    
    def schedule_weekday_runs(self, time_str="09:00"):
        """
        Schedule the pipeline to run on weekdays only
        """
        schedule.every().monday.at(time_str).do(self.run_daily_pipeline)
        schedule.every().tuesday.at(time_str).do(self.run_daily_pipeline)
        schedule.every().wednesday.at(time_str).do(self.run_daily_pipeline)
        schedule.every().thursday.at(time_str).do(self.run_daily_pipeline)
        schedule.every().friday.at(time_str).do(self.run_daily_pipeline)
        logging.info(f"Scheduled weekday pipeline to run at {time_str}")
    
    def run_scheduler(self):
        """
        Run the scheduler loop
        """
        logging.info("Starting scheduler...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def get_next_run(self):
        """
        Get information about the next scheduled run
        """
        jobs = schedule.get_jobs()
        if jobs:
            next_job = jobs[0]
            return {
                'next_run': next_job.next_run,
                'interval': str(next_job.interval),
                'unit': next_job.unit
            }
        return None

def main():
    """
    Main function to run the scheduler
    """
    scheduler = NewsScheduler()
    
    # Schedule daily runs (weekdays at 9 AM)
    scheduler.schedule_weekday_runs("09:00")
    
    # Run immediately for testing (comment out in production)
    # scheduler.run_daily_pipeline()
    
    # Start the scheduler
    try:
        scheduler.run_scheduler()
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Scheduler error: {e}")

if __name__ == "__main__":
    main() 