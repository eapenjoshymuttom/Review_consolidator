from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import traceback
import bot
import features
# import reviewExtractor

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ProductQuery(BaseModel):
    product_name: str

class ReviewQuery(BaseModel):
    product_name: str
    query: str

class UserPreferences(BaseModel):
    writing_style: str
    preferred_length: str
    focus_areas: List[str]

class ReviewText(BaseModel):
    text: str

class GenerateTemplateRequest(BaseModel):
    product_name: str
    writing_style: str
    preferred_length: str
    focus_areas: List[str]

@app.options("/product_summary")
@app.options("/component_ratings")
@app.options("/answer_query")
@app.options("/personalize_review_style")
@app.options("/text_completion")
@app.options("/real_time_feedback")
@app.options("/generate_review_template")
async def options_handler():
    return {"message": "OK"}

@app.post("/product_summary")
async def get_product_summary(product_query: ProductQuery):
    """Fetch product summary, price, and image."""
    try:
        name = product_query.product_name
        db, price, image_url = bot.get_or_create_db(name)
        if db is None:
            raise HTTPException(status_code=404, detail="No reviews found for this product.")
        
        summary = bot.get_product_summary(db, name)

        return {
            "summary": summary,
            "price": price,
            "image_url": image_url
        }

    except Exception as e:
        print(f"Error in get_product_summary: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/component_ratings")
async def get_component_ratings(product_query: ProductQuery):
    try:
        db, price, image_url = bot.get_or_create_db(product_query.product_name)
        if db is None:
            raise HTTPException(status_code=404, detail="No reviews found for this product.")
        
        ratings = bot.extract_component_ratings(db, product_query.product_name)
        print(f"Component ratings: {ratings}")  # Add logging
        return {
            "ratings": ratings,
            "price": price,
            "image_url": image_url
        }
    except Exception as e:
        print(f"Error in get_component_ratings: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer_query")
async def answer_query(review_query: ReviewQuery):
    try:
        # Unpack all three returned values
        db, price, image_url = bot.get_or_create_db(review_query.product_name)
        if db is None:
            raise HTTPException(status_code=404, detail="No reviews found for this product.")
            
        answer, _ = bot.get_response_from_query(db, review_query.query)
        return {"answer": answer}
    except Exception as e:
        print(f"Error in answer_query: {str(e)}")  # Add logging
        print(traceback.format_exc())  # Print full traceback
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/personalize_review_style")
async def personalize_style(preferences: UserPreferences):
    try:
        print(f"Received preferences: {preferences}")  # Log incoming data
        style_suggestion = features.personalize_review_style(preferences.dict())
        print(f"Generated style suggestion: {style_suggestion}")  # Log generated suggestion
        return {"style_suggestion": style_suggestion}
    except Exception as e:
        print(f"Error in personalize_style: {str(e)}")
        print(traceback.format_exc())  # Print full traceback
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text_completion")
async def complete_text(review_text: ReviewText):
    try:
        completion = features.text_completion(review_text.text)
        return {"completion": completion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/real_time_feedback")
async def get_feedback(review_text: ReviewText):
    try:
        feedback = features.real_time_feedback(review_text.text)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_review_template")
async def get_review_template(request: GenerateTemplateRequest):
    try:
        preferences = {
            "writing_style": request.writing_style,
            "preferred_length": request.preferred_length,
            "focus_areas": request.focus_areas
        }
        template = features.generate_review_template(request.product_name, preferences)
        return {"template": template}
    except Exception as e:
        print(f"Error in get_review_template: {str(e)}")  # Add this line for debugging
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)