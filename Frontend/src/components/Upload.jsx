import React, { useState } from "react";

function Upload({ onUpload, onClose }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = () => {
    if (!file) {
      alert("Please select a document.");
      return;
    }

    onUpload(file);
  };

  return (
    <div className="modal-overlay">

      <div className="upload-modal">

        <button
          className="modal-close"
          onClick={onClose}
        >
          ×
        </button>

        <div className="upload-modal-icon">
          📤
        </div>

        <h2>
          Upload Document
        </h2>

        <p>
          Add a document to your RAG knowledge base.
        </p>

        <label className="file-upload-area">

          <span className="large-upload-icon">
            📁
          </span>

          <strong>
            {file
              ? file.name
              : "Choose a document"}
          </strong>

          <small>
            PDF, TXT, DOCX
          </small>

          <input
            type="file"
            accept=".pdf,.txt,.docx"
            onChange={handleFileChange}
          />

        </label>

        <button
          className="upload-confirm-button"
          onClick={handleUpload}
        >
          Upload Document
        </button>

      </div>

    </div>
  );
}

export default Upload;