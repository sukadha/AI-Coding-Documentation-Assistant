import React, { useState } from "react";

import Sidebar from "./components/Sidebar";
import Chat from "./components/Chat";
import Upload from "./components/Upload";

import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All Documents");
  const [showUpload, setShowUpload] = useState(false);

  const [documentCounts, setDocumentCounts] = useState({
    all: 12,
    python: 5,
    sql: 3,
    machineLearning: 4,
    git: 2,
    api: 3,
    github: 1,
  });

  // Ask question to FastAPI backend
  const askQuestion = async (question) => {
    if (!question.trim()) {
      return;
    }

    // Add user message
    const userMessage = {
      type: "user",
      text: question,
    };

    setMessages((previous) => [...previous, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || data.message || "Something went wrong"
        );
      }

      console.log("Backend response:", data);

      // Backend answer
      const assistantMessage = {
        type: "assistant",

        // Your backend may return answer as a string
        text:
          data.answer ||
          data.response ||
          data.message ||
          "No answer returned from the backend.",

        // Sources returned by RAG
        sources: data.sources || [],
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (error) {
      console.error("API Error:", error);

      const errorMessage = {
        type: "assistant",
        text:
          "Unable to connect to the backend. Please make sure FastAPI is running on http://127.0.0.1:8000.",
        sources: [],
        error: true,
      };

      setMessages((previous) => [...previous, errorMessage]);
    }
  };

  // Upload document
  const uploadDocument = async (file) => {
    if (!file) {
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      console.log("Upload response:", data);

      if (!response.ok) {
        throw new Error(
          data.detail || data.message || "Upload failed"
        );
      }

      // Increase document count
      setDocumentCounts((previous) => ({
        ...previous,
        all: previous.all + 1,
      }));

      alert(
        data.message ||
          `${file.name} uploaded successfully`
      );

      setShowUpload(false);
    } catch (error) {
      console.error("Upload Error:", error);

      alert(
        "Upload failed. Make sure POST /api/upload is implemented in FastAPI."
      );
    }
  };

  return (
    <div className="app">

      {/* Sidebar */}
      <Sidebar
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
        documentCounts={documentCounts}
        messages={messages}
        setMessages={setMessages}
        onUploadClick={() => setShowUpload(true)}
      />

      {/* Main Content */}
      <main className="main-content">

        {/* Header */}
        <header className="top-header">

          <div className="brand-section">
            <div className="brand-icon">
              📖
            </div>

            <div>
              <h1>AI Coding Documentation Assistant</h1>

              <p>
                Ask questions from your own documentation and codebase
              </p>
            </div>
          </div>

          <div className="header-actions">

            <button className="header-btn active">
              🏠 Home
            </button>

            <button className="header-btn">
              🐙 GitHub
            </button>

            <button className="header-btn">
              📄 Docs
            </button>

            <button className="theme-btn">
              ☀️
            </button>

          </div>

        </header>

        {/* Upload Success / Information */}
        <div className="success-banner">

          <div className="success-icon">
            ✓
          </div>

          <div className="success-text">

            <strong>
              {documentCounts.all} documents loaded successfully!
            </strong>

            <span>
              Python documentation, SQL, Machine Learning,
              Git, API documentation and more.
            </span>

          </div>

          <button
            className="source-button"
            onClick={() => setSelectedCategory("All Documents")}
          >
            📁 View Sources
          </button>

        </div>

        {/* Chat */}
        <Chat
          messages={messages}
          askQuestion={askQuestion}
        />

      </main>

      {/* Upload Modal */}
      {showUpload && (
        <Upload
          onUpload={uploadDocument}
          onClose={() => setShowUpload(false)}
        />
      )}

    </div>
  );
}

export default App;