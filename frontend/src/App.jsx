import React, { useState, useRef, useEffect } from "react";

export default function App() {
  const [input, setInput] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const chatEndRef = useRef(null);

  // Generate a unique session ID once per user (simple UUID here)
  const [sessionId] = useState(() => {
    // Try to get from localStorage or create new
    let sid = localStorage.getItem("session_id");
    if (!sid) {
      sid = crypto.randomUUID();
      localStorage.setItem("session_id", sid);
    }
    return sid;
  });

  const sendMessage = async () => {
    if (!input.trim()) return;

    setChatLog((prev) => [...prev, { sender: "user", text: input }]);

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: input, session_id: sessionId }),
      });

      const data = await response.json();

      if (response.ok) {
        setChatLog((prev) => [...prev, { sender: "ai", text: data.response }]);
      } else {
        setChatLog((prev) => [
          ...prev,
          { sender: "ai", text: data.error || "Something went wrong." },
        ]);
      }
    } catch (error) {
      setChatLog((prev) => [
        ...prev,
        { sender: "ai", text: "Failed to connect to server." },
      ]);
    }

    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  // Auto scroll chat to bottom when chatLog changes
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatLog]);

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "auto",
        padding: 20,
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h2>LangGraph Chatbot</h2>
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: 8,
          padding: 10,
          height: 400,
          overflowY: "auto",
          marginBottom: 10,
          backgroundColor: "#f9f9f9",
        }}
        aria-label="Chat history"
      >
        {chatLog.map((msg, i) => (
          <div
            key={i}
            style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              marginBottom: 8,
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 20,
                backgroundColor: msg.sender === "user" ? "#007bff" : "#e5e5ea",
                color: msg.sender === "user" ? "#fff" : "#000",
                maxWidth: "80%",
                wordWrap: "break-word",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <input
        type="text"
        placeholder="Type your message"
        aria-label="Type your message"
        autoFocus
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        style={{
          width: "100%",
          padding: "10px",
          fontSize: "16px",
          borderRadius: "20px",
          border: "1px solid #ccc",
          boxSizing: "border-box",
        }}
      />
      <button
        onClick={sendMessage}
        style={{
          marginTop: 10,
          padding: "10px 20px",
          fontSize: "16px",
          borderRadius: "20px",
          border: "none",
          backgroundColor: "#007bff",
          color: "white",
          cursor: "pointer",
        }}
      >
        Send
      </button>
    </div>
  );
}
