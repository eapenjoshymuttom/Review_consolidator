**Review Summarizer**

Review Summarizer is a web-based application designed to automate the summarization of Amazon product reviews, providing users with meaningful, concise summaries to help make informed purchasing decisions.
By leveraging web scraping, natural language processing (NLP), and machine learning, Review Summarizer efficiently distills product reviews and allows users to interact with a chatbot powered by Groq Llama3 for additional product insights.

**Features**

  **1. Web Scraping:** Retrieves reviews from Amazon using aiohttp and BeautifulSoup.
  
  **2. Summarization:** Uses NLP techniques to generate concise summaries that focus on key product details.
  
  **3. Chatbot Integration:** Includes a chatbot powered by Groq Llama3, enabling users to ask product-related questions.
  
  **4. User Interface:** A responsive web interface allows users to input product names, view summaries, and interact with the chatbot.
  
  **5. Graphical Insights:** Provides graphical summaries on specific features like battery life, performance, and user satisfaction.


**Usage**

  **1. Input Product:** On the homepage, enter the product name you want to retrieve reviews for.
  
  **2. View Summary:** The system will scrape, process, and display a summary of the reviews.
  
  **3. Chatbot Interaction:** Ask product-specific questions to the chatbot for more insights.
  
  **4. Graphical Insights:** View graphs detailing specific product features based on user feedback.
  

**Technologies Used**

  **1. Python:** Programming language for backend processing.
  
  **2. FastAPI:** Backend framework for building the API.
  
  **3. aiohttp & BeautifulSoup:** Used for web scraping Amazon reviews.
  
  **4. Groq Llama3:** Language model powering the chatbot.
  
  **5. NLP Models:** For summarizing reviews and analyzing sentiments.
  
  **6. React:** Frontend library for user interaction.
  
  **7. Matplotlib:** For generating graphs in product analysis.