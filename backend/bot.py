import os
import reviewExtractor
import price_comparison
import warnings
from transformers import AutoTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from groq import Groq
import pickle

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

def create_db_from_reviews(reviews: list) -> FAISS:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=8)
    docs = text_splitter.create_documents(reviews)
    print("number of docs:", len(docs))
    db = FAISS.from_documents(docs, embeddings)
    return db

def save_db(db, product_name):
    if not os.path.exists('product_dbs'):
        os.makedirs('product_dbs')
    filename = f"product_dbs/{product_name.replace(' ', '_').lower()}_faiss_index.pkl"
    with open(filename, "wb") as f:
        pickle.dump(db, f)

def load_db(product_name):
    filename = f"product_dbs/{product_name.replace(' ', '_').lower()}_faiss_index.pkl"
    with open(filename, "rb") as f:
        return pickle.load(f)

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
        db = load_db(product_name)
        print(f"Loaded existing FAISS database for {product_name}.")
        price, image_url = reviewExtractor.get_product_details(product_name)
    except FileNotFoundError:
        print(f"No existing database found for {product_name}. Creating new database from reviews.")
        result = reviewExtractor.extractReviews(product_name)
        
        # Use processed reviews directly
        db = create_db_from_reviews(result['processed_reviews'])
        save_db(db, product_name)
        
        price = result['price']
        image_url = result['image_url']
        print(f"New database created and saved for {product_name}.")
    
    return db, price, image_url


def handle_user_queries(db):
    while True:
        question = input("\nEnter your question about the product (or 'quit' to exit): ")
        if question.lower() == 'quit':
            print("Exiting the query session.")
            break

        answer, _ = get_response_from_query(db, question)
        print("\nAnswer:", answer)

def main(product_name):
    db = get_or_create_db(product_name)

    # Get and print product summary
    print("\nProduct Summary:")
    summary = get_product_summary(db, product_name)
    print(summary)
    # price_comparison.priceComparison(product_name)

    handle_user_queries(db)

if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    main(product_name)