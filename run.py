#!/usr/bin/env python3
"""
News Headline Summarizer - Main Run Script
Provides easy access to all components of the system
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print the application banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    📰 News Headline Summarizer               ║
    ║                                                              ║
    ║  Google News · MiniLM · KMeans · Gemini API · Streamlit     ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Creating from template...")
        if os.path.exists('env_example.txt'):
            with open('env_example.txt', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ Created .env file from template")
            print("📝 Please edit .env file and add your Gemini API key")
        else:
            print("❌ env_example.txt not found")
            return False
    
    # Check if data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        print("✅ Created data directory")
    
    return True

def run_dashboard():
    """Start the Streamlit dashboard"""
    print("🚀 Starting Streamlit dashboard...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

def run_scheduler():
    """Start the automated scheduler"""
    print("⏰ Starting automated scheduler...")
    try:
        subprocess.run([sys.executable, "scheduler.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Scheduler stopped by user")
    except Exception as e:
        print(f"❌ Error starting scheduler: {e}")

def run_test():
    """Run the test suite"""
    print("🧪 Running test suite...")
    try:
        subprocess.run([sys.executable, "test_pipeline.py"], check=True)
    except Exception as e:
        print(f"❌ Error running tests: {e}")

def run_manual_pipeline():
    """Run the pipeline manually"""
    print("🔄 Running manual pipeline...")
    try:
        from scheduler import NewsScheduler
        scheduler = NewsScheduler()
        scheduler.run_daily_pipeline()
    except Exception as e:
        print(f"❌ Error running pipeline: {e}")

def show_menu():
    """Show the main menu"""
    print("\n📋 Available Options:")
    print("1. 🚀 Start Dashboard (Streamlit)")
    print("2. ⏰ Start Scheduler (Automated)")
    print("3. 🔄 Run Manual Pipeline")
    print("4. 🧪 Run Tests")
    print("5. 📖 View README")
    print("6. 🛠️  Install Dependencies")
    print("0. 🚪 Exit")
    
    choice = input("\nSelect an option (0-6): ").strip()
    
    if choice == "1":
        run_dashboard()
    elif choice == "2":
        run_scheduler()
    elif choice == "3":
        run_manual_pipeline()
    elif choice == "4":
        run_test()
    elif choice == "5":
        show_readme()
    elif choice == "6":
        install_dependencies()
    elif choice == "0":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid option. Please try again.")

def show_readme():
    """Show the README content"""
    print("\n" + "="*60)
    print("📖 README Content:")
    print("="*60)
    
    if os.path.exists('README.md'):
        with open('README.md', 'r') as f:
            content = f.read()
            # Show first 500 characters
            print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("README.md not found")
    
    print("\n" + "="*60)

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")

def main():
    """Main function"""
    print_banner()
    
    # Check environment
    if not check_environment():
        print("❌ Environment setup failed. Please check the errors above.")
        return
    
    print("✅ Environment ready!")
    
    # Show menu
    while True:
        show_menu()
        
        # Ask if user wants to continue
        continue_choice = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
        if continue_choice == 'q':
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 