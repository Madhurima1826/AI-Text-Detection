import requests
from bs4 import BeautifulSoup
import re
import random  # Mocking AI detection
from pprint import pprint

# Function to extract blog content
def extract_blog_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the URL: {url}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Example: extracting content within <p> tags
    paragraphs = soup.find_all('p')
    blog_content = ' '.join([para.get_text() for para in paragraphs])
    
    return blog_content

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Mock function to detect AI-generated content (replace with a real model or API)
def detect_ai_generated_content(text):
    # Random score for illustration (replace with real detection logic)
    score = random.uniform(0, 1)
    return score

# Function to detect AI-generated content using an external API
def detect_ai_content_with_api(blog_content):
    response = requests.post(
        "https://api.sapling.ai/api/v1/aidetect",
        json={
            "key": "A2E6QGJM452LJ8S00WM9CORRZPD6IICQ",
            "text": blog_content
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the API: {response.status_code}")
    
    return response.json()

# Main function
def main():
    url = "https://hevodata.com/learn/snowpipe-alternatives/"  # Replace with the actual blog URL
    try:
        blog_content = extract_blog_content(url)
        blog_content = preprocess_text(blog_content)
        
        # Detect AI-generated content using mock function
        score = detect_ai_generated_content(blog_content)
        
        print(f"Blog content: {blog_content[:500]}...")  # Print a snippet of the blog content
        print(f"AI-generated content score: {score:.2f}")
        
        if score > 0.5:
            print("The content is likely AI-generated.")
        else:
            print("The content is likely human-written.")
        
        # Detect AI-generated content using external API
        api_result = detect_ai_content_with_api(blog_content)
        pprint(api_result)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
