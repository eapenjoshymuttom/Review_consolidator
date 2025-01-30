from datetime import datetime
import time
import re
import random
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import linkExtractor
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Header to set the requests as a browser request
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def modify_reviews_url(reviews_url):
    """Convert product URL to reviews URL format"""
    return reviews_url.replace("/dp/", "/product-reviews/")

def get_base_url(url):
    """Extract the base URL without pagination parameters"""
    if '&pageNumber=' in url:
        return url.split('&pageNumber=')[0]
    return url

def reviewsHtml(reviews_url, url, len_page=None):
    """
    Extract HTML data from multiple pages of Amazon reviews
    Args:
        reviews_url: Base URL of the product reviews page
        url: Original product URL
        len_page: Maximum number of pages to scrape (None for all pages)
    """
    soups = []
    page_no = 1

    while True:
        # Add random delay to avoid getting blocked
        time.sleep(random.uniform(1, 3))

        # Set page number in the request params
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,
        }

        try:
            # Make request for each page
            response = requests.get(url, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Save HTML object using BeautifulSoup and lxml parser
                soup = BeautifulSoup(response.text, 'lxml')

                # Check if there are any reviews on the page
                if not soup.select('div[data-hook="review"]'):
                    print(f"No more reviews found on page {page_no}. Stopping.")
                    break

                # Add single HTML page data to master list
                soups.append(soup)
                print(f"Successfully scraped page {page_no}")

                # Break if we've reached len_page
                if len_page and page_no >= len_page:
                    break

                page_no += 1

            else:
                print(f"Failed to fetch page {page_no}. Status code: {response.status_code}")
                break

        except requests.RequestException as e:
            print(f"Error fetching page {page_no}: {e}")
            break

    return soups

def getReviews(html_data):
    data_dicts = []
    boxes = html_data.select('div[data-hook="review"]')  # Updated selector

    for box in boxes:
        try:
            # Name
            name = box.select_one('.a-profile-name').text.strip()

            # Stars
            stars_element = box.select_one('.a-icon-star')
            stars = stars_element.text.strip().split(' ')[0] if stars_element else 'N/A'

            # Title
            title = box.select_one('[data-hook="review-title"] span').text.strip()

            # Date
            date_element = box.select_one('[data-hook="review-date"]')
            date = date_element.text.split('on ')[-1] if date_element else 'N/A'

            # Description
            description = box.select_one('[data-hook="review-body"] span').text.strip()

            data_dicts.append({
                'Name': name,
                'Stars': stars,
                'Title': title,
                'Date': date,
                'Description': description
            })
            
        except Exception as e:
            print(f"Error processing review: {e}")
            continue
            
    return data_dicts

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = text.lower().strip()  # Convert to lowercase and strip whitespace
    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    return ' '.join(word for word in text.split() if word not in stop_words)

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    return ' '.join(lemmatizer.lemmatize(word) for word in text.split())

def split_sentences(reviews):
    sentences = []
    for review in reviews:
        sentences.extend(sent_tokenize(review))
    return sentences

def remove_duplicates(reviews):
    return list(set(reviews))

def filter_short_reviews(reviews, min_length=10):
    return [review for review in reviews if len(review.split()) >= min_length]

def preprocess_reviews(reviews):
    reviews = [clean_text(review) for review in reviews]
    reviews = [remove_stopwords(review) for review in reviews]
    reviews = [lemmatize_text(review) for review in reviews]
    reviews = split_sentences(reviews)
    reviews = remove_duplicates(reviews)
    reviews = filter_short_reviews(reviews)
    return reviews

def extractReviews(product_name, len_page=5):
    """
    Main function to extract reviews from Amazon
    Args:
        product_name: Product name to search for
        len_page: Maximum number of pages to scrape (None for all pages)
    """
    # Get all product links
    product_links = linkExtractor.get_product_links(product_name)

    # Create an empty list to hold all reviews data
    all_reviews = []

    # Iterate through each product link
    for url in product_links:
        # URL of the Amazon review page
        reviews_url = modify_reviews_url(url)
        base_url = get_base_url(reviews_url)

        print(f"Scraping reviews for: {base_url}")

        # Grab all HTML data
        html_datas = reviewsHtml(reviews_url, url, len_page)

        # Iterate over all HTML pages and gather review data
        for html_data in html_datas:
            reviews = getReviews(html_data)
            if reviews:
                all_reviews.extend(reviews)  # Append reviews to the master list

    # Create a DataFrame with all reviews data
    df_reviews = pd.DataFrame(all_reviews)

    # Print the DataFrame
    print(df_reviews)

    if not os.path.exists('reviews'):
        os.makedirs('reviews')
    # Save data to CSV with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'reviews/{product_name}_reviews_{timestamp}.csv'
    df_reviews.to_csv(filename, index=False)
    print(f"Saved {len(all_reviews)} reviews to {filename}")

    # Preprocess reviews
    reviews = df_reviews['Description'].tolist()
    reviews = preprocess_reviews(reviews)

    return reviews

# Example usage
# if __name__ == "__main__":
#     product_name = "iphone 13"  # Example product name
#     reviews = extractReviews(product_name, len_page=10)  # Set len_page=None to scrape all pages