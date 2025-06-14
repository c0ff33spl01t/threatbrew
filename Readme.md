ThreatBrew: AI-Powered Cybersecurity News Digest
ThreatBrew is a Python-based automation tool that scans cybersecurity news feeds, uses the Google Gemini API to generate strategic summaries of relevant articles, and emails a daily digest to a list of recipients. It's designed to save security leaders and teams time by delivering concise, relevant, and actionable intelligence directly to their inboxes.

Features
RSS Feed Aggregation: Monitors multiple cybersecurity news sources.
Keyword Filtering: Scans articles for user-defined keywords (e.g., "ransomware", "CISO", "vulnerability").
AI-Powered Summarization: Leverages Google's Gemini model to create structured, strategic summaries.
Deduplication: Ensures that the same story from different sources only appears once.
Email Digest: Sends a professionally formatted HTML email to a list of recipients as a Blind Carbon Copy (BCC) for privacy.
Setup and Installation

1. Prerequisites
   Python 3.9 or higher.
   A Google Account with a Gemini API key.
   A Gmail account with an App Password enabled for sending emails.
2. Clone the Repository
   After creating your repository on GitHub, clone it to your local machine:

git clone <your-repository-url>
cd <your-repository-name>

3. Create a Virtual Environment
   It is highly recommended to use a virtual environment to manage dependencies.

# Create the virtual environment

python3 -m venv venv

# Activate it (on macOS/Linux)

source venv/bin/activate

# Or activate it (on Windows)

.\venv\Scripts\activate

4. Install Dependencies
   Install all required Python packages using the requirements.txt file.

pip install -r requirements.txt

5. Set Up Environment Variables
   This script uses environment variables to securely manage your API keys and credentials.
   Copy the example file:
   cp setupEnv.sh.example setupEnv.sh

Edit setupEnv.sh with your favorite text editor and replace the placeholder values with your actual credentials.
GOOGLE_API_KEY: Your key from Google AI Studio.
EMAIL_SENDER: Your full Gmail address.
EMAIL_PASSWORD: Your 16-digit Gmail App Password.
EMAIL_RECIPIENT: A comma-separated list of emails to send the digest to.
Load the variables into your terminal session. You must do this every time you open a new terminal.
source setupEnv.sh

Usage
Once your environment is set up and the variables are loaded, simply run the script:

python threatbrew.py

The script will print its progress to the console and send an email if any relevant articles are found.

Customization
You can easily customize the script by editing the threatbrew.py file:
RSS_FEEDS: Add or remove RSS feed URLs from this list.
KEYWORDS: Modify the list of keywords to match your interests.
Prompt: Edit the prompt inside the get_gemini_summary function to change the structure or focus of the AI-generated summaries.
