import React from "react";

function Sidebar({
  selectedCategory,
  setSelectedCategory,
  documentCounts,
  messages,
  setMessages,
  onUploadClick,
}) {
  const categories = [
    {
      name: "All Documents",
      icon: "📄",
      count: documentCounts.all,
    },
    {
      name: "Python",
      icon: "🐍",
      count: documentCounts.python,
    },
    {
      name: "SQL",
      icon: "🗄️",
      count: documentCounts.sql,
    },
    {
      name: "Machine Learning",
      icon: "🧠",
      count: documentCounts.machineLearning,
    },
    {
      name: "Git",
      icon: "🔀",
      count: documentCounts.git,
    },
    {
      name: "API Documentation",
      icon: "</>",
      count: documentCounts.api,
    },
    {
      name: "GitHub Repository",
      icon: "🐙",
      count: documentCounts.github,
    },
  ];

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <aside className="sidebar">

      {/* Upload */}
      <button
        className="upload-main-button"
        onClick={onUploadClick}
      >
        <span>⬆</span>
        <span>Upload Document</span>
        <span className="upload-arrow">⌄</span>
      </button>

      {/* Knowledge Base */}
      <div className="sidebar-section">

        <h3>Knowledge Base</h3>

        {categories.map((category) => (
          <button
            key={category.name}
            className={`category-item ${
              selectedCategory === category.name
                ? "selected"
                : ""
            }`}
            onClick={() =>
              setSelectedCategory(category.name)
            }
          >

            <span className="category-icon">
              {category.icon}
            </span>

            <span className="category-name">
              {category.name}
            </span>

            <span className="category-count">
              {category.count}
            </span>

          </button>
        ))}

      </div>

      {/* Recent Conversations */}
      <div className="sidebar-section recent-section">

        <h3>Recent Conversations</h3>

        {messages.length === 0 ? (
          <div className="no-conversations">
            No recent conversations
          </div>
        ) : (
          <div className="conversation-item">

            <span className="conversation-icon">
              💬
            </span>

            <div>
              <strong>
                {messages[0]?.text?.slice(0, 30)}
              </strong>

              <small>
                Recent
              </small>
            </div>

          </div>
        )}

      </div>

      {/* Clear Chat */}
      <button
        className="clear-chat-button"
        onClick={clearChat}
      >
        🗑 Clear Chat
      </button>

    </aside>
  );
}

export default Sidebar;