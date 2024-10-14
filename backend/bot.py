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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
    docs = text_splitter.create_documents(reviews)
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

def get_response_from_query(db, query, k=8):
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    prompt = f'''You are a helpful assistant that can answer questions about product reviews. Answer the following question: {query} 
                 Based on the following reviews: {docs_page_content} 
                 Only use factual information from the reviews to answer the question.'''

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.66,
        max_tokens=3990,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response, docs

def get_product_summary(db):
    summary_query = "Provide a comprehensive summary of the product based on all reviews."
    summary, _ = get_response_from_query(db, summary_query, k=10)  # Use more reviews for the summary
    return summary

def get_or_create_db(product_name):
    try:
        db = load_db(product_name)
        print(f"Loaded existing FAISS database for {product_name}.")
    except FileNotFoundError:
        print(f"No existing database found for {product_name}. Creating new database from reviews.")
        reviews = reviewExtractor.extractReviews(product_name)
        db = create_db_from_reviews(reviews)
        save_db(db, product_name)
        print(f"New database created and saved for {product_name}.")
    return db

def main(product_name):
    db = get_or_create_db(product_name)

    # Get and print product summary
    print("\nProduct Summary:")
    summary = get_product_summary(db)
    print(summary)
    # price_comparison.priceComparison(product_name)

    while True:
        question = input("\nEnter your question about the product (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break

        answer, _ = get_response_from_query(db, question)
        print("\nAnswer:", answer)

if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    main(product_name)