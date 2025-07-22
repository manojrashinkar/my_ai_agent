from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
import os

load_dotenv(override=True)
openai = OpenAI()

reader = PdfReader("Profile.pdf")
linkedin = "Profile.pdf"
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text
print(linkedin)
with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()
name = "Manoj Rashinkar"
system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."
system_prompt += f"With this context, please chat if you dont have information about me replay asking Please ask about career only"
print(system_prompt)
google_api_key = os.getenv('GOOGLE_API_KEY')
if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")
def chat(message, history):
    
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

    gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    model_name = "gemini-2.0-flash"
    response = gemini.chat.completions.create(model=model_name, messages=messages)
    return response.choices[0].message.content
# gr.ChatInterface(chat, type="messages").launch()
gr.ChatInterface(
    chat,
    type="messages",
    title="👨‍💼 Ask Me Anything - ManojGPT",
    description="I'm your personalized AI agent. Ask anything about Manoj's career, skills, or journey!"
).launch()

    # display(Markdown(answer))
  
