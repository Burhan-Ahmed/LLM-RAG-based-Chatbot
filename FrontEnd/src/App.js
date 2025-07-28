import React, { useState, useEffect } from "react";
import "./App.css";
import "bootstrap-icons/font/bootstrap-icons.css";

function App() {
  const [question, setQuestion] = useState("");      // User's input
  const [loading, setLoading] = useState(false);     // Loading spinner
  const [greeting, setGreeting] = useState("");      // Welcome text
  const [chatHistory, setChatHistory] = useState([]); // Stores all messages

  // Load saved chats and greeting on first render
  useEffect(() => {
    const savedChats = localStorage.getItem("crickchat-history");
    if (savedChats) {
      setChatHistory(JSON.parse(savedChats));
    }

    setGreeting(
      "👋 Hello! I'm CrickChat - your friendly PCB cricket assistant. Ask me anything about Pakistani players — stats, profiles, or recent matches!"
    );
  }, []);

  // Save chat history to localStorage whenever it changes
  useEffect(() => {
    console.log("chatHistory updated:", chatHistory);
    localStorage.setItem("crickchat-history", JSON.stringify(chatHistory));
  }, [chatHistory]);

   const handleStop = () => {
  setLoading(false);

};

  
  // Handle form submit (text query)
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    // Save user's message
    setChatHistory((prev) => [...prev, { role: "user", message: question }]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      // Save bot's response
      setChatHistory((prev) => [...prev, { role: "bot", message: data.answer }]);
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        { role: "bot", message: "❌ Failed to fetch response." },
      ]);
    }

    setLoading(false);
    setQuestion("");
  };

  // Handle voice input
  const handleVoiceClick = async () => {
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/voice");
      const data = await res.json();

      if (data.answer) {
        setChatHistory((prev) => [
          ...prev,
          { role: "user", message: "🎤 Voice Input" },
          { role: "bot", message: data.answer },
        ]);
      } else {
        setChatHistory((prev) => [
          ...prev,
          { role: "bot", message: data.error || "❌ Voice recognition failed." },
        ]);
      }
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { role: "bot", message: "❌ Voice recognition failed. Please try again." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <h1>🏏 CrickChat</h1>
      <p className="greeting">{greeting}</p>

      {/* Display chat history */}
      <div className="response">
      <div className="chat-history">
  {chatHistory.map((chat, index) => (
    <div key={index} className={`chat-message ${chat.role}`}>
      <p>
        <strong>{chat.role === "user" ? "You" : "CrickChat"}:</strong>{" "}
        {chat.message}
      </p>
    </div>
  ))}
  {loading && (
    <div className="chat-message bot">
      <p>🔄 Generating...</p>
    </div>
  )}
</div>

      </div>

      {/* Input and mic button */}
      <form onSubmit={handleSubmit} className="chat-form">
        <div className="input-container">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about Pakistani players..."
          />
          {loading ? (
  <button type="button" onClick={handleStop} className="stop-button">
    <i className="bi bi-stop-circle-fill"></i>
  </button>
) : (
  <button type="submit" className="send-button">
    <i className="bi bi-arrow-up-circle-fill"></i>
  </button>
)}
          <button
            type="button"
            onClick={handleVoiceClick}
            className="mic-button"
          >
            <i className="bi bi-mic"></i>
          </button>
        </div>
      </form>
    </div>
  );
}

export default App;
