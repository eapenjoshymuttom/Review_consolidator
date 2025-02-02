import os
import reviewExtractor
import warnings
import json
from transformers import AutoTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from groq import Groq
import pickle
import re

# Load environment variables from .env file
load_dotenv()

# Suppress FutureWarnings related to tokenization
warnings.simplefilter(action='ignore', category=FutureWarning)

# Load your tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2', clean_up_tokenization_spaces=True)

# Initialize Groq client
groq_api_key = os.getenv("GROQCLOUD_API_KEY")
client = Groq(api_key=groq_api_key)

# Initialize HuggingFaceEmbeddings with the loaded tokenizer
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

def sanitize_filename(filename):
    """Sanitize the filename by replacing invalid characters and spaces with underscores."""
    return re.sub(r'[\\/*?:"<>| ]', '_', filename)

def create_db_from_reviews(reviews: list) -> FAISS:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=8)
    docs = text_splitter.create_documents(reviews)
    print("number of docs:", len(docs))
    db = FAISS.from_documents(docs, embeddings)
    return db

def save_db(db, product_name, price, image_url):
    if not os.path.exists('product_dbs'):
        os.makedirs('product_dbs')
    sanitized_name = sanitize_filename(product_name)
    filename = f"product_dbs/{sanitized_name}_faiss_index.pkl"
    with open(filename, "wb") as f:
        pickle.dump({'db': db, 'price': price, 'image_url': image_url}, f)

def load_db(product_name):
    sanitized_name = sanitize_filename(product_name)
    filename = f"product_dbs/{sanitized_name}_faiss_index.pkl"
    with open(filename, "rb") as f:
        data = pickle.load(f)
        return data['db'], data['price'], data['image_url']

def get_response_from_query(db, query):
    docs = db.similarity_search(query, k=150)
    docs_page_content = " ".join([d.page_content for d in docs])

    prompt = f'''
                You are an assistant that answers questions based on product reviews. Below are customer reviews about a product.
                Answer the following question based on the reviews:
                Question: {query}
                Here are the reviews: {docs_page_content}
                Provide a concise and specific answer to the question.'''

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=1500,
        top_p=1,
    )

    response = completion.choices[0].message.content.strip()
    return response, docs

def get_product_summary(db, product_name):
    docs = db.similarity_search(product_name, k=150)
    docs_page_content = " ".join([d.page_content for d in docs])

    prompt = f'''
                You are an assistant that summarizes product reviews. Below are customer reviews about a product.
                Summarize the reviews focusing on:
                1. **Key Features**: Highlight commonly mentioned features.
                2. **Problems**: List recurring issues.
                3. **Rating**: Provide an overall rating out of 5.
                Here are the reviews: {docs_page_content}
                Provide the summary and rating now.'''

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=1500,
        top_p=1,
    )

    response = completion.choices[0].message.content.strip()
    return response

def get_or_create_db(product_name):
    try:
        db, price, image_url = load_db(product_name)
        print(f"Loaded existing FAISS database for {product_name}.")
    except FileNotFoundError:
        print(f"No existing database found for {product_name}. Creating new database from reviews.")
        result = reviewExtractor.extractReviews(product_name)
        
        # Use processed reviews directly
        db = create_db_from_reviews(result['processed_reviews'])
        save_db(db, product_name, result['price'], result['image_url'])
        
        price = result['price']
        image_url = result['image_url']
        print(f"New database created and saved for {product_name}.")
    
    return db, price, image_url

def get_or_create_db_from_link(product_link):
    try:
        db, price, image_url = load_db(product_link)
        print(f"Loaded existing FAISS database for {product_link}.")
    except FileNotFoundError:
        print(f"No existing database found for {product_link}. Creating new database from reviews.")
        result = reviewExtractor.extractReviewsFromLink(product_link)
        
        # Use processed reviews directly
        db = create_db_from_reviews(result['processed_reviews'])
        save_db(db, product_link, result['price'], result['image_url'])
        
        price = result['price']
        image_url = result['image_url']
        print(f"New database created and saved for {product_link}.")
    
    return db, price, image_url

def extract_component_ratings(db, product_name):
    """Extract ratings for different components from product reviews."""
    # Get relevant reviews
    docs = db.similarity_search(product_name, k=150)
    docs_content = " ".join([d.page_content for d in docs])
    
    prompt = f'''
    Analyze these product reviews and extract ratings for different components.
    For a {product_name}, identify the main components (e.g., camera, battery, performance)
    and provide an average rating out of 5 for each component based on the reviews.
    
    Reviews: {docs_content}
    
    Return the results in this exact format:
    {{
        "component_ratings": [
            {{"name": "Component1", "rating": X.X}},
            {{"name": "Component2", "rating": X.X}},
            ...
        ],
        "overall_rating": X.X
    }}
    '''
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
    )
    
    try:
        # Log the response content for debugging
        response_content = completion.choices[0].message.content.strip()
        print(f"Response content: {response_content}")
        
        # Extract the JSON part from the response content
        json_start = response_content.find('{')
        json_end = response_content.rfind('}') + 1
        json_content = response_content[json_start:json_end]
        
        # Parse the JSON content and return it
        response = json.loads(json_content)
        return response
    except Exception as e:
        print(f"Error parsing component ratings: {str(e)}")
        return {
            "component_ratings": [],
            "overall_rating": 0
        }

def handle_user_queries(db):
    while True:
        question = input("\nEnter your question about the product (or 'quit' to exit): ")
        if question.lower() == 'quit':
            print("Exiting the query session.")
            break

        answer, _ = get_response_from_query(db, question)
        print("\nAnswer:", answer)

def main(product_name):
    db, price, image_url = get_or_create_db(product_name)

    # Get and print product summary
    print("\nProduct Summary:")
    summary = get_product_summary(db, product_name)
    print(summary)

    handle_user_queries(db)

if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    main(product_name)