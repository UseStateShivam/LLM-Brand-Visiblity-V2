import os
from dotenv import load_dotenv
from google import genai

if __name__ == "__main__":
    loaded = load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="What is the age of the sun?",
    )

    print(response.text)