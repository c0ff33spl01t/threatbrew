import feedparser
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai 
import os

# --- Configuration (Unchanged) ---
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackerNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss_simple.asp"
]
KEYWORDS = ["ransomware", "ciso", "data breach", "cloud security", "vulnerability"]

# --- Secure Loading ---
try:
    GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
    EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
   # EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT")
   # 1. Get the comma-separated string of recipients from the environment variable.
    email_recipient_str = os.environ.get("EMAIL_RECIPIENT", "")
    # 2. Split the string into a clean list of emails.
    RECIPIENT_LIST = [email.strip() for email in email_recipient_str.split(',') if email.strip()]

except (KeyError, TypeError) as e:
    print(f"Error: Environment variable not set or invalid.")
    exit()

# --- Workflow Logic ---
def get_and_process_feeds():
    # This part of the logic remains the same
    found_articles = []
    processed_titles = set()
    for feed_url in RSS_FEEDS:
        print(f"Processing feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            normalized_title = title.strip().lower()
            if normalized_title in processed_titles:
                continue
            content_to_scan = f"{title.lower()} {getattr(entry, 'summary', '').lower()}"
            if any(keyword in content_to_scan for keyword in KEYWORDS):
                print(f"  -> Found relevant article: {title}")
                processed_titles.add(normalized_title)
                
                # We call the new, rewritten function here
                ai_summary = get_gemini_summary_new(entry.link, entry.summary)
                
                if ai_summary:
                    found_articles.append({"title": title, "link": entry.link, "summary": ai_summary})
    return found_articles

# --- Gemini Function (Rewritten to match your snippet) ---
def get_gemini_summary_new(url, summary_text):
    """
    Calls the Gemini API using the genai.Client pattern you provided.
    """
    try:
        # 1. Initialize the client as shown in your documentation
        client = genai.Client(api_key=GEMINI_API_KEY)

        # 2. Construct the prompt
        prompt = f"""
        You are tasked with analyzing the cybersecurity article provided in the summary and URL below. Your analysis should support strategic decision-making for a security leader.

          Instructions:

          1. Provide a 3-Bullet Summary:
            - Summarize the article in exactly three bullet points.
            - Each bullet should reflect a distinct, critical insight from the article.
            - Focus on strategic relevance or emerging risk.
            - Use clear language that is easy to understand for business and security leaders.
            - Rename this 3-Bullet Summary to Summary, use Bold format and Heading level 3

          2. Key Takeaway (for a Security Leader):
            - Write a single sentence identifying the most important strategic insight from the article.
            - This should help guide risk prioritization, strategic planning, or resource allocation.
            - Rename this section to just Key Takeaway, use Bold Format and heading level 3


          Important Notes:
          - Maintain a strategic focus. Avoid overly technical jargon unless necessary.
          - Emphasize organizational impact and implications for defense posture.
          - This summary will be sent in an email, the content need to be easy to digest and visualize

        URL for context: {url}
        Article Summary: "{summary_text}"
        """
        
        # 3. Call the function with the model as a parameter
        # Using the full model name is safer for preview models.
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-preview-05-20",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        print(f"    An error occurred with the genai.Client method: {e}")
        return None

def send_summary_email(articles, recipient_list):
    """
    Formats and sends an email with the collected articles, converting
    Markdown to HTML for proper formatting.
    """
    if not articles:
        print("No new articles found to email.")
        return

    subject = f"ThreatBrew Report: {len(articles)} Unique Analyses"
    recipient_str_for_header = ", ".join(recipient_list)
    # Basic CSS for better readability of the generated HTML
    html_body = """
    <html>
      <head>
        <style>
          body { font-family: sans-serif; line-height: 1.6; }
          h2 { font-size: 18px; margin-bottom: 5px; }
          .article { margin-bottom: 25px; border-bottom: 1px solid #eee; padding-bottom: 15px; }
          .summary-content ul { margin-top: 5px; padding-left: 20px; }
          .summary-content p { margin-top: 5px; }
        </style>
      </head>
      <body>
    """
    html_body += f"<h1>Your daily ThreatBrew Report</h1><p>Freshly brewed by Anon. Here are the {len(articles)} unique, relevant analyses for today.</p><hr>"

    for article in articles:
        # ---- THIS IS THE KEY CHANGE ----
        # Convert the Markdown summary from Gemini into proper HTML
        html_summary = markdown.markdown(article['summary'])
        
        html_body += f"""
        <div class="article">
            <h2><a href="{article['link']}" style="color: #0056b3; text-decoration: none;">{article['title']}</a></h2>
            <div class="summary-content">
                {html_summary}
            </div>
        </div>
        """
    html_body += "</body></html>"
    
    message = MIMEMultipart()
    message['From'] = EMAIL_SENDER
    message['To'] = EMAIL_SENDER
    message['Subject'] = subject
    message.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient_list, message.as_string())
            print(f"\nEmail successfully sent to {recipient_str_for_header}!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# --- Main Execution Block ---
if __name__ == "__main__":
    articles_to_email = get_and_process_feeds()
    if articles_to_email:
        # We need to make sure the email function is not omitted
        # For now, let's just print a success message.
        print(f"\nSuccessfully generated summaries for {len(articles_to_email)} articles.")
        send_summary_email(articles_to_email, RECIPIENT_LIST) # You would uncomment this
    else:
        print("Finished processing. No relevant articles to email today.")