import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

import linkExtractor

# Header to set the requests as a browser request
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def modify_reviews_url(reviews_url):
    return reviews_url.replace("/dp/", "/product-reviews/")

# Define the number of pages to scrape (initial assumption)
len_page = 10

# Function to extract data as an HTML object from the Amazon review page
def reviewsHtml(reviews_url, url, len_page):

    # Empty list to store all pages' HTML data
    soups = []

    # Loop to gather reviews from all pages
    for page_no in range(1, len_page + 1):

        # Set page number in the request params
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,  # Add page number to fetch the next page
        }

        # Make request for each page
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Save HTML object using BeautifulSoup and lxml parser
            soup = BeautifulSoup(response.text, 'lxml')

            # Check if there are any reviews on the page (stop if no reviews are found)
            if not soup.select('div[data-hook="review"]'):
                print(f"No more reviews found on page {page_no}. Stopping.")
                break

            # Add single HTML page data to master list
            soups.append(soup)
        else:
            print(f"Failed to fetch page {page_no}. Status code: {response.status_code}")
            break  # Stop the loop if there is an issue with pagination

    return soups

# Function to grab reviews: name, description, date, stars, title from HTML
def getReviews(html_data):

    # Create an empty list to hold all data
    data_dicts = []

    # Select all reviews box HTML using CSS selector
    boxes = html_data.select('div[data-hook="review"]')

    # If there are no review boxes, stop further processing for this page
    if not boxes:
        return None

    # Iterate over all review boxes 
    for box in boxes:

        # Extract name, stars, title, date, description, handling exceptions
        try:
            name = box.select_one('[class="a-profile-name"]').text.strip()
        except Exception:
            name = 'N/A'

        try:
            stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
        except Exception:
            stars = 'N/A'   

        try:
            title = box.select_one('[data-hook="review-title"]').text.strip()
        except Exception:
            title = 'N/A'

        try:
            datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
            date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
        except Exception:
            date = 'N/A'

        try:
            description = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception:
            description = 'N/A'

        # Create dictionary with all review data
        data_dict = {
            'Name': name,
            'Stars': stars,
            'Title': title,
            'Date': date,
            'Description': description
        }

        # Add dictionary to master list
        data_dicts.append(data_dict)

    return data_dicts

def extractReviews(product_name):
    # URL of the Amazon product page
    url = linkExtractor.get_product_links(product_name)[0]

    # URL of the Amazon review page
    reviews_url = modify_reviews_url(url)

    # Define the number of pages to scrape (initial assumption)
    len_page = 10

    # Grab all HTML data
    html_datas = reviewsHtml(reviews_url, url, len_page)

    # Create an empty list to hold all reviews data
    reviews = []

    # Iterate over all HTML pages and gather review data
    for html_data in html_datas:
        review = getReviews(html_data)
        if review:
            reviews += review  # Only append reviews if the page contains reviews

    # Create a DataFrame with reviews data
    df_reviews = pd.DataFrame(reviews)

    # Create a DataFrame with reviews data
    df_reviews = pd.DataFrame(reviews)

    print(df_reviews)

    # Save data to CSV
    df_reviews.to_csv('reviews.csv', index=False)
    value = df_reviews['Description'].tolist()

    return value

