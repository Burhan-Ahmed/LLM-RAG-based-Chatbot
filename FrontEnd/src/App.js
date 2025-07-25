import React, { useState, useEffect } from "react";
import "./App.css";
import "bootstrap-icons/font/bootstrap-icons.css";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    // Greet the user when the app loads
    setGreeting(
      "👋 Hello! I'm CrickChat - your friendly PCB cricket assistant. Ask me anything about Pakistani players — stats, profiles, or recent matches!"
    );
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setResponse("");

    try {
      const res = await fetch("https://mburhannahmed-chatbot.hf.space/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      setResponse(data.answer);
    } catch (err) {
      setResponse(
        "❌ Error connecting to the server. Make sure the Flask backend is running."
      );
    }

    setLoading(false);
    setQuestion("");
  };

  const handleVoiceClick = () => {
    setResponse("🎤 Listening...");
    setLoading(true);

    const recognition = new window.webkitSpeechRecognition(); // For Chrome
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = async (event) => {
      const spokenText = event.results[0][0].transcript;
      setQuestion(spokenText);

      try {
        const res = await fetch("https://mburhannahmed-chatbot.hf.space/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: spokenText }),
        });

        const data = await res.json();
        setResponse(data.answer);
      } catch (err) {
        setResponse("❌ Error reaching the backend.");
      }

      setLoading(false);
    };

    recognition.onerror = (err) => {
      setLoading(false);
      setResponse("❌ Voice recognition failed.");
      console.error("Speech recognition error:", err);
    };

    recognition.start();
  };

  return (
    <div className="App">
      <h1>🏏 CrickChat</h1>
      <p className="greeting">{greeting}</p>

      <form onSubmit={handleSubmit} className="chat-form">
        <div className="input-container">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about Pakistani players..."
          />
          <button
            type="button"
            onClick={handleVoiceClick}
            className="mic-button"
          >
            <i className="bi bi-mic"></i>
          </button>
        </div>
        <button type="submit" disabled={loading}>
          Ask
        </button>
      </form>

      <div className="response">
        {loading ? <p>🔄 Thinking...</p> : <p>{response}</p>}
      </div>
    </div>
  );
}

export default App;
