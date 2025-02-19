from datetime import datetime
import time
import re
import random
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from linkExtractor import get_product_links

# Download necessary NLTK datasets
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Headers to avoid request blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# -------------------- REVIEW EXTRACTION --------------------
def modify_reviews_url(reviews_url):
    """Convert product URL to reviews URL format"""
    return reviews_url.replace("/p/", "/product-reviews/")

def get_reviews_from_page(html):
    """Extract reviews from a single Flipkart page."""
    reviews_data = []
    review_containers = html.find_all('div', {'class': 'cPHDOP'})  # Flipkart review container
    
    for container in review_containers:
        try:
            # Extract rating
            rating_div = container.find('div', {'class': 'XQDdHH Ga3i8K'})
            rating = rating_div.text.strip() if rating_div else 'N/A'
            
            # Extract review title
            title_div = container.find('p', {'class': 'z9E0IG'})
            title = title_div.text.strip() if title_div else 'N/A'
            
            # Extract review text
            review_div = container.find('div', {'class': 'ZmyHeo'})
            review_text = review_div.find('div').text.strip() if review_div and review_div.find('div') else 'N/A'
            
            # Extract reviewer name
            name_div = container.find('p', {'class': '_2NsDsF AwS1CA'})
            name = name_div.text.strip() if name_div else 'N/A'
            
            # Extract review date
            date_div = container.find('p', {'class': '_2NsDsF'})
            date = date_div.text.strip() if date_div and not date_div.get('class') == '_2NsDsF AwS1CA' else 'N/A'
            
            # Extract certified buyer status
            certified_div = container.find('p', {'class': 'MztJPv'})
            is_certified = 'Yes' if certified_div and 'Certified Buyer' in certified_div.text else 'No'
            
            # Get helpful votes
            helpful_div = container.find('span', {'class': 'tl9VpF'})
            helpful_count = helpful_div.text.strip() if helpful_div else '0'
            
            reviews_data.append({
                'Name': name,
                'Rating': rating,
                'Title': title,
                'Description': review_text,
                'Date': date,
                'Certified_Buyer': is_certified,
                'Helpful_Votes': helpful_count
            })
            
        except Exception as e:
            print(f"Error processing review: {e}")
            continue
    
    return reviews_data

def get_reviews(base_url, max_pages=10):
    """Extract reviews from multiple pages."""
    all_reviews = []
    page = 1
    
    while page <= max_pages:
        try:
            # Construct page URL
            page_url = f"{base_url}&page={page}" if page > 1 else base_url
                
            print(f"Fetching reviews from page {page}")
            
            response = requests.get(page_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}. Status code: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"Page HTML length: {len(response.content)}")  # Debug info
            
            # Get reviews from current page
            page_reviews = get_reviews_from_page(soup)
            
            if not page_reviews:
                print(f"No reviews found on page {page}")
                break
                
            all_reviews.extend(page_reviews)
            print(f"Successfully scraped {len(page_reviews)} reviews from page {page}")
            
            # Random delay to avoid being blocked
            time.sleep(random.uniform(2, 4))
            page += 1
            
        except Exception as e:
            print(f"Error processing page {page}: {e}")
            break
    
    return all_reviews

def get_product_details(product_url):
    """Extract product price and image from Flipkart."""

    if not isinstance(product_url, str) or not product_url.startswith('http'):
        print(f"Invalid product URL: {product_url}")
        return "N/A", "N/A"
    
    print(f"\nFetching product details from: {product_url}")
    
    try:
        response = requests.get(product_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch product page. Status code: {response.status_code}")
            return "N/A", "N/A"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract price with better error handling
        try:
            price_div = soup.find('div', {'class': 'Nx9bqj'})
            price = price_div.text.strip() if price_div else "N/A"
        except Exception as e:
            print(f"Error extracting price: {e}")
            price = "N/A"

        # Extract product image with better error handling
        try:
            img_tag = soup.find('img', {'class': 'DByuf4 IZexXJ jLEJ7H'})
            image_url = img_tag['src'] if img_tag else "N/A"
        except Exception as e:
            print(f"Error extracting image: {e}")
            image_url = "N/A"
        
        return price, image_url

    except Exception as e:
        print(f"Error fetching product details: {e}")
        return "N/A", "N/A"

# -------------------- PREPROCESSING --------------------

def clean_text(text):
    """Clean the review text."""
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'READ MORE', '', text, flags=re.IGNORECASE)  # Remove "READ MORE"
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)  # Remove special characters but keep punctuation
    text = ' '.join(text.split())  # Normalize whitespace
    return text.strip()

def remove_stopwords(text):
    """Remove stopwords from text."""
    stop_words = set(stopwords.words('english'))
    return ' '.join(word for word in text.split() if word.lower() not in stop_words)

def lemmatize_text(text):
    """Lemmatize words in text."""
    lemmatizer = WordNetLemmatizer()
    return ' '.join(lemmatizer.lemmatize(word) for word in text.split())

def preprocess_reviews(reviews):
    """Apply preprocessing pipeline to reviews."""
    processed_reviews = []
    for review in reviews:
        # Clean text
        cleaned = clean_text(review)
        # Remove stopwords & lemmatize
        processed_review = lemmatize_text(remove_stopwords(cleaned))
        if len(processed_review.split()) >= 3:  # Keep only meaningful reviews
            processed_reviews.append(processed_review)
    
    return processed_reviews

# -------------------- MAIN FUNCTION --------------------

def extractReviews(name, max_pages=15):
    """Extract Flipkart reviews and product price."""
    links = get_product_links(name)
    
    if not links:
        print("No product links found!")
        return [], "N/A", "N/A"

    all_reviews = []
    
    # Iterate through each product link
    for link in links:  # Only process first link to avoid duplicates
        url = modify_reviews_url(link)
        print(f"\nExtracting reviews from: {url}") 
    
        # Get reviews
        product_reviews = get_reviews(url, max_pages)
        if product_reviews:
            all_reviews.extend(product_reviews)

    if not all_reviews:
        print("No reviews found!")
        return [], "N/A", "N/A"
    
    # Save raw reviews
    if not os.path.exists('reviews'):
        os.makedirs('reviews')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_filename = f'reviews/{name}_flipkart_reviews{timestamp}.csv'
    df_reviews = pd.DataFrame(all_reviews)
    
    df_reviews.to_csv(raw_filename, index=False)
    print(f"\nSaved {len(all_reviews)} raw reviews to {raw_filename}")

    # Preprocess review descriptions
    processed_reviews = preprocess_reviews(df_reviews['Description'].tolist())

    # Fetch product details from the first valid product link
    price, image_url = get_product_details(links[0])

    return {
        'raw_reviews': all_reviews,
        'processed_reviews': processed_reviews,
        'price': price,
        'image_url': image_url
    }

def sanitize_filename(filename):
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', filename)
    return sanitized[:100]  # Truncate to 100 characters

def extractReviewsFromLink(link, max_pages=15):
    sanitized_link = sanitize_filename(link)  # Sanitize FULL link first

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    raw_filename = f'reviews/{sanitized_link}_flipkart_reviews{timestamp}.csv'
    all_reviews = []
    
    url = modify_reviews_url(link)
    print(f"\nExtracting reviews from: {url}") 
    
    # Get reviews
    product_reviews = get_reviews(url, max_pages)
    if product_reviews:
        all_reviews.extend(product_reviews)

    if not all_reviews:
        print("No reviews found!")
        return [], "N/A", "N/A"
    
    # Save raw reviews
    if not os.path.exists('reviews'):
        os.makedirs('reviews')
    
    sanitized_link = sanitize_filename(link.split("/")[-1])
    raw_filename = f'reviews/{sanitized_link}_flipkart_reviews{timestamp}.csv'
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(raw_filename), exist_ok=True)
    
    df_reviews = pd.DataFrame(all_reviews)
    df_reviews.to_csv(raw_filename, index=False)
    print(f"\nSaved {len(all_reviews)} raw reviews to {raw_filename}")

    # Preprocess review descriptions
    processed_reviews = preprocess_reviews(df_reviews['Description'].tolist())

    # Fetch product details from the link
    price, image_url = get_product_details(link)

    return {
        'raw_reviews': all_reviews,
        'processed_reviews': processed_reviews,
        'price': price,
        'image_url': image_url
    }
