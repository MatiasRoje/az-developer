import React, { useState } from "react";

export const ImageUpload: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div className="max-w-2xl mx-auto">
      <div className="azure-card p-8 text-center">
        <h2 className="text-2xl font-bold text-neutral-900 mb-4">Upload Images</h2>
        <p className="text-neutral-600 mb-8">
          Upload your images to Azure Blob Storage and process them with Azure Functions
        </p>
        
        <div
          className={`border-2 border-dashed rounded-lg p-12 transition-colors ${
            isDragging
              ? "border-azure-400 bg-azure-50"
              : "border-neutral-300 hover:border-azure-300"
          }`}
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDragging(false);
            // TODO: Handle file drop
          }}
        >
          <div className="text-6xl text-neutral-400 mb-4">📁</div>
          <p className="text-lg font-medium text-neutral-700 mb-2">
            Drop images here or click to browse
          </p>
          <p className="text-neutral-500">
            Supports JPG, PNG, GIF up to 10MB
          </p>
          <button className="azure-button-primary mt-6">
            Choose Files
          </button>
        </div>
      </div>
    </div>
  );
}; 