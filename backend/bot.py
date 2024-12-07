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

def get_response_from_query(db, query, k):
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    prompt = f'''
                    You are a highly capable and analytical assistant that helps summarize product reviews accurately. Below, you'll find a set of customer reviews about a specific product.
                    Your task is to generate a detailed and comprehensive summary focusing on three main aspects:
                    1. **Key Product Features**: Identify and highlight the most commonly mentioned features of the product, such as its performance, design, durability, battery life, display, etc.
                        Be sure to include both positive aspects and standout features that multiple users have praised.
                    2. **Common Problems or Complaints**: List any recurring issues or problems reported by users.
                        These may include concerns about product quality, performance failures, design flaws, shipping problems, or any other negative experiences mentioned in the reviews.
                    3. **Overall Rating**: Based on the overall sentiment of the reviews, assign the product a rating out of 5, with 5 being excellent and 1 being very poor.
                        This rating should reflect the general customer satisfaction with the product.
                    Make sure to summarize the information in a clear, concise manner using only factual data from the reviews.
                    Your analysis should be structured into three sections: 'Features,' 'Problems,' and 'Rating,' with bullet points under the first two categories. Use neutral and professional language.
                    And if the provided reviews do not mention any specific features or problems, you can still generate a summary based on the available information.
                    Here are the customer reviews: {docs_page_content}.
                    Even if the provided customer reviews are incomplete or repetition of the same phrases, you should still generate a summary based on the available information.
                    Provide the summary and rating now.'''


    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.66,
        max_tokens=4590,
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
    summary, _ = get_response_from_query(db, summary_query, k=100)  # Use more reviews for the summary
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