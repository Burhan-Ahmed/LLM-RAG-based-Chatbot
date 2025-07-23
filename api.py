from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
from fastapi.responses import JSONResponse
from chatbot import ask_crickchat  # assuming your logic is in voice.py

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 👈 React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define request model (you mistakenly called it ChatRequest later)
class Message(BaseModel):
    question: str

# ✅ Optional: Greeting endpoint
@app.get("/")
def home():
    return {"message": "🚀 CrickChat API is running! Use POST /chat to ask questions."}

# ✅ Chat endpoint
@app.post("/chat")
def chat_endpoint(req: Message):  # 👈 Fix: Use `Message` not `ChatRequest`
    print("Received:", req)
    response = ask_crickchat(req.question)
    return {"answer": response}

# @app.get("/voice")
# def voice_chat():
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()

#     try:
#         with mic as source:
#             print("🎤 Listening for voice input...")
#             recognizer.adjust_for_ambient_noise(source)
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
#             user_text = recognizer.recognize_google(audio)
#             print("Recognized:", user_text)

#             # 👇 Feed into your main model function
#             response = ask_crickchat(user_text)
#             return {"answer": response}

#     except sr.UnknownValueError:
#         return JSONResponse(status_code=400, content={"answer": "❌ Sorry, I couldn't understand your voice."})
#     except sr.WaitTimeoutError:
#         return JSONResponse(status_code=408, content={"answer": "⌛ Timeout — no speech detected."})
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"answer": f"❌ Error: {str(e)}"})
