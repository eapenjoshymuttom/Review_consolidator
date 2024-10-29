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
        prompt = f"""
                    You are an assistant that helps write product reviews. Based on these preferences: {user_preferences}, suggest a personalized review style.
                    Include:
                    1. **Tone**: Formal, casual, etc.
                    2. **Structure**: Overall opinion, pros and cons, conclusion.
                    3. **Focus Areas**: Key features or problems.
                    4. **Rating**: Suggested rating out of 5.
                    Here are the preferences: {user_preferences}
                    Provide the review style now.
                    """
        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.2,
            max_tokens=600,
            top_p=1,
        )
        
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in personalize_review_style: {str(e)}")
        raise  # Re-raise the exception to be caught by the FastAPI error handler

def text_completion(current_text):
    prompt = f"""
                You are an assistant that completes product reviews. Below is a partial review.
                Complete it by:
                1. **Matching Tone**: Keep the same tone.
                2. **Reflecting Insights**: Include key features or problems.
                3. **Balancing Opinion**: Balance pros and cons.
                4. **Concluding**: Finish with a strong conclusion.
                Here is the partial review: {current_text}
                Provide the continuation now.
                """
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=700,
        top_p=1,
    )
    
    return completion.choices[0].message.content.strip()

def real_time_feedback(review_text):
    prompt = f"""
                You are an assistant that provides feedback on product reviews. Below is a draft review.
                Provide feedback on:
                1. **Clarity**: Is it clear?
                2. **Detail**: Enough details?
                3. **Balance**: Balanced pros and cons?
                4. **Tone and Structure**: Logical flow?
                5. **Overall Suggestions**: Final tips.
                Here is the draft review: {review_text}
                Provide feedback now.
                """
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=850,
        top_p=1,
    )
    
    return completion.choices[0].message.content.strip()

def generate_review_template(product_name, user_preferences):
    prompt = f"""
                You are an assistant that creates product review templates. Based on the product: {product_name} and these preferences: {user_preferences}, generate a template.
                Include:
                1. **Introduction**: Brief overview.
                2. **Pros**: Positive aspects.
                3. **Cons**: Negative aspects.
                4. **Detailed Features**: Specific features.
                5. **Overall Impression**: Summary and rating.
                Here is the product: {product_name} and preferences: {user_preferences}
                Provide the template now.
                """
    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=500,
        top_p=1,
    )
    
    return completion.choices[0].message.content.strip()