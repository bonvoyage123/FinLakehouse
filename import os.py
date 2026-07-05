import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(
    "You are a coding agent. Help me debug this repository and suggest the next best fix."
)

print(response.text)