import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

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

# Function to submit content to QuillBot's AI Content Detector
def submit_to_quillbot(blog_content):
    url = "https://quillbot.com/ai-content-detector"  # QuillBot's AI Content Detector URL
    
    # Start a session to handle cookies and headers
    session = requests.Session()
    
    # Fetch the initial page to get cookies and any necessary headers
    response = session.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to access QuillBot page: {response.status_code}")
    
    # Prepare data for submission
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    payload = {
        "text": blog_content,
    }
    
    # Submit the content
    response = session.post(url, data=payload, headers=headers)
    if response.status_code == 403:
        print("Access forbidden. The request might be blocked or restricted.")
        return "Access forbidden. The request might be blocked or restricted."
    elif response.status_code != 200:
        raise Exception(f"Failed to submit content: {response.status_code}")
    
    # Parse the result
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the result based on the page's structure
    # This requires inspecting the actual page to find the correct element containing the result
    result_element = soup.find("div", class_="result-class")  # Replace with actual class or ID from QuillBot
    if result_element:
        result_text = result_element.get_text(strip=True)
        return result_text
    else:
        return "Result not found"

# Main function to process each URL from the CSV
def main():
    # Read URLs from CSV file
    urls_df = pd.read_csv('Demo.csv')
    
    for url in urls_df['url']:
        try:
            print(f"Processing URL: {url}")
            
            # Extract and preprocess blog content
            blog_content = extract_blog_content(url)
            blog_content = preprocess_text(blog_content)
            
            print(f"Blog content: {blog_content[:500]}...")  # Print a snippet of the blog content
            
            # Submit content to QuillBot's AI Content Detector
            result = submit_to_quillbot(blog_content)
            print("QuillBot Result:")
            print(result)
        
        except Exception as e:
            print(f"An error occurred with URL {url}: {e}")

if __name__ == "__main__":
    main()
