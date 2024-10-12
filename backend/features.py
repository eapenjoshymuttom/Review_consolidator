import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_api_key = os.getenv("GROQCLOUD_API_KEY")
client = Groq(api_key=groq_api_key)

def personalize_review_style(user_preferences):
    try:
        prompt = f"""Based on the following user preferences: {user_preferences},
        suggest a personalized review style for writing product reviews."""
        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200,
            top_p=1,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in personalize_review_style: {str(e)}")
        print(traceback.format_exc())
        raise  # Re-raise the exception to be caught by the FastAPI error handler

def text_completion(current_text):
    prompt = f"""Complete the following product review:
    {current_text}
    Provide a natural continuation of the review."""
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100,
        top_p=1,
    )
    
    return completion.choices[0].message.content

def real_time_feedback(review_text):
    prompt = f"""Analyze the following product review and provide constructive feedback:
    {review_text}
    Consider aspects like detail, clarity, and balance of positive and negative points."""
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150,
        top_p=1,
    )
    
    return completion.choices[0].message.content

def generate_review_template(product_name, user_preferences):
    prompt = f"""Create a review template for the product: {product_name}
    Consider the following user preferences: {user_preferences}
    The template should include sections for pros, cons, and overall impression."""
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
        top_p=1,
    )
    
    return completion.choices[0].message.content