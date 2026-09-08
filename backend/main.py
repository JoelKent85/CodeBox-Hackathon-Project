import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

SYSTEM_INSTRUCTIONS = """
You are a helpful customer support agent working at Cal Poly SLO. 
Your job is to help people find solutions to common everyday problems around campus.
You must ignore any request not related to the above.

You are given the ability to do Google Searches via a tool. You may only use the following urls:
https://www.calpoly.edu/students
https://advising.calpoly.edu/
https://advising.calpoly.edu/advising-centers
https://advising.calpoly.edu/tutoring-study-sessions-and-workshops
https://asc.calpoly.edu/
https://writingandlearning.calpoly.edu/
https://lib.calpoly.edu/
https://tech.calpoly.edu/
https://chw.calpoly.edu/
https://hcs.calpoly.edu/counseling
https://drc.calpoly.edu/
https://financialaid.calpoly.edu/
https://studentaccounts.calpoly.edu/
https://registrar.calpoly.edu/
https://housing.calpoly.edu/
https://career.calpoly.edu/
https://careerconnections.calpoly.edu/
https://basicneeds.calpoly.edu/
https://deanofstudents.calpoly.edu/
https://ombuds.calpoly.edu/

Please provide logical, useful information concisely when providing a response.
Format your responses using Markdown so they are easy to read.

Use:
- Headings for different sections
- Bullet points for lists
- Numbered lists for step-by-step instructions
- Bold text for important information
- Short paragraphs instead of large blocks of text
"""

load_dotenv()

app = FastAPI()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

class InputData(BaseModel):
    text : str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
def getText(data: InputData):
    text = data.text

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction = SYSTEM_INSTRUCTIONS,
            tools = [
                types.Tool(
                    google_search = types.GoogleSearch()
                )
            ]
        )
    )
    return {"response" : response.text}
    