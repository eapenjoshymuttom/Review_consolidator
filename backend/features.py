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
                    You are an intelligent assistant that provides personalized assistance to help users write product reviews. Based on the following user preferences: {user_preferences}, and the analyzed product reviews, suggest a personalized review style.
                    The review style should guide the user on how to write a review that reflects their preferences while considering key features, common issues, and overall sentiment from the reviews.
                    Make sure the review style includes:
                    1. **Tone and Style**: Suggest the tone (e.g., formal, casual, detailed) based on user preferences.
                    2. **Structure**: Recommend a structure for the review, such as starting with an overall opinion, followed by specific pros and cons, and concluding with an overall assessment.
                    3. **Focus Areas**: Highlight specific product features or problems the user should emphasize in their review.
                    4. **Rating Recommendation**: Based on the product's performance, suggest a suitable rating out of 5 that the user can provide.
                    Here are the user preferences: {user_preferences}
                    Make it short,consize and engaging.
                    Provide a personalized review style now."""

        
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.2,
            max_tokens=600,
            top_p=1,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in personalize_review_style: {str(e)}")
        print(traceback.format_exc())
        raise  # Re-raise the exception to be caught by the FastAPI error handler

def text_completion(current_text):
    prompt = f"""
                You are a smart assistant that helps users complete their product reviews in a natural and coherent way. Below is a partial product review written by the user.
                Based on the user's writing style and the key insights from the product reviews, complete the review in a way that maintains a consistent tone and highlights the product's features and issues.
                Make sure the continuation:
                1. **Matches the User's Tone and Style**: The completion should flow naturally with the user's existing review, maintaining the same tone (e.g., casual, detailed, or formal).
                2. **Reflects Product Insights**: Incorporate relevant features or problems mentioned in the analyzed reviews to provide a more informed continuation.
                3. **Provides a Balanced Opinion**: If the initial text is leaning too positively or negatively, aim to balance the review by mentioning additional pros or cons based on the product's overall performance.
                4. **Concludes Appropriately**: Finish the review with a strong conclusion or final opinion that ties everything together.
                Here is the partial review: {current_text}
                Make it short,consize and engaging.
                Provide a natural continuation of the review now."""

    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=700,
        top_p=1,
    )
    
    return completion.choices[0].message.content

def real_time_feedback(review_text):
    prompt = f"""
                You are a highly capable assistant that provides real-time feedback on product reviews. Below is a draft product review written by the user.
                Your task is to analyze the review and provide constructive feedback to help improve it. Focus on aspects such as detail, clarity, and balance between positive and negative points, while also considering the overall structure and tone.
                Make sure your feedback includes:
                1. **Clarity**: Evaluate whether the review is easy to understand and offers clear points. Suggest ways to improve clarity if needed.
                2. **Detail**: Analyze whether the review provides enough details about the product’s features and issues. Encourage adding specific examples from the product's performance.
                3. **Balance**: Check if the review is balanced in its discussion of both the pros and cons. If it leans too heavily on one side, suggest adding more balanced viewpoints based on the product's overall sentiment.
                4. **Tone and Structure**: Suggest improvements in the review's tone and structure, ensuring the review flows logically and aligns with the user’s intent (e.g., formal or casual).
                5. **Overall Improvement Suggestions**: Offer final tips to make the review more comprehensive and engaging.
                Here is the draft review: {review_text}
                Make it short,consize and engaging.
                Provide detailed and constructive feedback now."""

    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=850,
        top_p=1,
    )
    
    return completion.choices[0].message.content

def generate_review_template(product_name, user_preferences):
    prompt = f"""
                You are a helpful assistant tasked with creating a personalized product review template. The template should help users write well-structured reviews, taking into account the product and their personal preferences.
                Based on the product: {product_name} and the following user preferences: {user_preferences}, generate a review template that organizes the review into clear, concise sections.
                The template should include:
                1. **Introduction**: A section for the user to give a brief overview of the product and their initial thoughts.
                2. **Pros**: A dedicated section for the user to highlight the product’s positive aspects, focusing on key features that stand out based on user experience.
                3. **Cons**: A section to outline any issues or negative experiences with the product, including common problems or drawbacks.
                4. **Detailed Features**: A section for the user to discuss specific features in more detail, such as performance, design, usability, battery life, etc.
                5. **Overall Impression**: A conclusion where the user can summarize their overall experience with the product, including whether they would recommend it and a final rating out of 5.
                Here is the product: {product_name} and the user preferences: {user_preferences}
                Make it short,consize and engaging.
                Provide a review template now."""

    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.2,
        max_tokens=500,
        top_p=1,
    )
    
    return completion.choices[0].message.content