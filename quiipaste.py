import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from pprint import pprint

# Function to extract blog content and concatenate into a single sentence
def extract_blog_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the URL: {url}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract content within <p> tags and concatenate into a single sentence
    paragraphs = soup.find_all('p')
    blog_content = ' '.join([para.get_text().replace('.', '').replace('\n', '') for para in paragraphs])
    
    return blog_content

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Function to detect AI-generated content using an external API
def detect_ai_content_with_api(blog_content):
    response = requests.post(
        "https://api.sapling.ai/api/v1/aidetect",
        json={
            "key": "BUVLMC1YY4O24MICZMX5MTVXXS8FVUKG",
            "text": blog_content
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the API: {response.status_code}")
    
    api_response = response.json()
    overall_score = api_response.get('score', 'Score not available')
    return overall_score

# Main function to process each URL from the CSV
def main():
    # Read URLs from CSV file
    urls_df = pd.read_csv('Demo.csv')
    
    # Initialize an empty list to store results
    results = []

    for url in urls_df['url']:
        try:
            print(f"Processing URL: {url}")
            
            # Extract and preprocess blog content
            blog_content = extract_blog_content(url)
            blog_content = preprocess_text(blog_content)
            
            # Detect AI-generated content using external API
            score = detect_ai_content_with_api(blog_content)
            
            # Append result to the list
            results.append({'url': url, 'score': score})
            print(f"Overall Score: {score}")
        
        except Exception as e:
            print(f"An error occurred with URL {url}: {e}")
            # Append error result to the list
            results.append({'url': url, 'score': 'Error'})

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Merge results with original DataFrame
    updated_df = urls_df.merge(results_df, on='url', how='left')
    
    # Save updated DataFrame to CSV
    updated_df.to_csv('Demo.csv', index=False)

if __name__ == "__main__":
    main()
