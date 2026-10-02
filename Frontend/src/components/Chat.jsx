import React, { useState } from "react";
import SourceCard from "./SourceCard";

function Chat({ messages, askQuestion }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setLoading(true);

    await askQuestion(question);

    setQuestion("");
    setLoading(false);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  return (
    <section className="chat-container">

      {/* Chat messages */}
      <div className="messages-area">

        {messages.length === 0 && (
          <div className="welcome-container">

            <div className="welcome-icon">
              🤖
            </div>

            <h2>
              Ask your coding question
            </h2>

            <p>
              Ask questions about Python, SQL,
              Machine Learning, Git, APIs and your
              documentation.
            </p>

            <div className="example-questions">

              <button
                onClick={() =>
                  setQuestion("What is Python?")
                }
              >
                What is Python?
              </button>

              <button
                onClick={() =>
                  setQuestion(
                    "What are the common data types in Python?"
                  )
                }
              >
                What are Python data types?
              </button>

              <button
                onClick={() =>
                  setQuestion(
                    "How are functions defined in Python?"
                  )
                }
              >
                How are functions defined?
              </button>

              <button
                onClick={() =>
                  setQuestion(
                    "What is the difference between a list and a dictionary?"
                  )
                }
              >
                List vs Dictionary
              </button>

            </div>

          </div>
        )}

        {messages.map((message, index) => (

          <div
            key={index}
            className={`message-row ${
              message.type === "user"
                ? "user-row"
                : "assistant-row"
            }`}
          >

            {/* User */}
            {message.type === "user" ? (

              <div className="user-message">
                {message.text}
              </div>

            ) : (

              <div className="assistant-message">

                <div className="bot-avatar">
                  🤖
                </div>

                <div className="answer-container">

                  <div
                    className={`answer ${
                      message.error
                        ? "error-answer"
                        : ""
                    }`}
                  >
                    {message.text}
                  </div>

                  {/* Sources */}
                  {message.sources &&
                    message.sources.length > 0 && (

                      <div className="sources-container">

                        <h3>
                          📚 Sources
                        </h3>

                        <div className="sources-grid">

                          {message.sources.map(
                            (source, sourceIndex) => (

                              <SourceCard
                                key={sourceIndex}
                                source={source}
                              />

                            )
                          )}

                        </div>

                      </div>

                    )}

                </div>

              </div>

            )}

          </div>

        ))}

      </div>

      {/* Question input */}
      <form
        className="question-form"
        onSubmit={handleSubmit}
      >

        <div className="input-wrapper">

          <span className="attachment-icon">
            📎
          </span>

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask your coding question here..."
            rows="1"
          />

        </div>

        <button
          className="send-button"
          type="submit"
          disabled={loading}
        >
          {loading ? "..." : "➤"}
        </button>

      </form>

    </section>
  );
}

export default Chat;