import React from "react";

function SourceCard({ source }) {
  const filename =
    source.filename ||
    source.file ||
    source.name ||
    "Unknown document";

  const page =
    source.page ||
    source.page_number ||
    null;

  const category =
    source.category ||
    "Documentation";

  return (
    <div className="source-card">

      <div className="source-file-icon">
        📄
      </div>

      <div className="source-info">

        <strong>
          {filename}
        </strong>

        <span>
          {category}
          {page ? ` • Page ${page}` : ""}
        </span>

      </div>

    </div>
  );
}

export default SourceCard;