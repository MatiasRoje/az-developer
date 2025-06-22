import React, { useState, useRef } from "react";
import {
  imageService,
  type ImageUploadResponse,
} from "../services/imageService";
import { useAuth } from "../hooks/useAuth";

export const ImageUpload: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string>("");
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<ImageUploadResponse | null>(
    null
  );
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { token } = useAuth();

  const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];
  const maxSize = 10 * 1024 * 1024; // 10MB

  const validateFile = (file: File): boolean => {
    setError("");

    if (!allowedTypes.includes(file.type)) {
      setError("Only JPG, JPEG, and PNG files are allowed");
      return false;
    }

    if (file.size > maxSize) {
      setError("File size must be less than 10MB");
      return false;
    }

    return true;
  };

  const handleFileSelect = (file: File) => {
    if (validateFile(file)) {
      setSelectedFile(file);
      setUploadResult(null);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleChooseFiles = () => {
    fileInputRef.current?.click();
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setError("");
    setUploadResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !token) {
      setError("Please select a file and ensure you're logged in");
      return;
    }

    setIsUploading(true);
    setError("");

    try {
      const result = await imageService.uploadImage(selectedFile, token);
      setUploadResult(result);
    } catch (error) {
      console.error("Upload error:", error);
      setError(error instanceof Error ? error.message : "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  // Show upload success state
  if (uploadResult) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="azure-card p-8 text-center">
          <h2 className="text-2xl font-bold text-neutral-900 mb-4">
            Upload Images
          </h2>
          <p className="text-neutral-600 mb-8">
            Upload your images to Azure Blob Storage and process them with
            Python Microservices
          </p>

          <div className="border-2 border-solid border-green-300 rounded-lg p-8 bg-green-50">
            <div className="text-6xl text-green-500 mb-4">🎉</div>
            <p className="text-lg font-medium text-neutral-700 mb-2">
              Upload Successful!
            </p>
            <div className="bg-white rounded-lg p-4 mb-4">
              <p className="font-medium text-neutral-800">
                Upload ID: {uploadResult.upload_id}
              </p>
              <p className="text-neutral-600">Status: {uploadResult.status}</p>
              <p className="text-sm text-neutral-500 mt-2">
                {uploadResult.message}
              </p>
            </div>
            <button className="azure-button-primary" onClick={handleRemoveFile}>
              Upload Another Image
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="azure-card p-8 text-center">
        <h2 className="text-2xl font-bold text-neutral-900 mb-4">
          Upload Images
        </h2>
        <p className="text-neutral-600 mb-8">
          Upload your images to Azure Blob Storage and process them with Python
          Microservices
        </p>

        {!selectedFile ? (
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
            onDrop={handleDrop}
          >
            <div className="text-6xl text-neutral-400 mb-4">📁</div>
            <p className="text-lg font-medium text-neutral-700 mb-2">
              Drop images here or click to browse
            </p>
            <p className="text-neutral-500">
              Supports JPG, JPEG, PNG up to 10MB
            </p>
            <button
              className="azure-button-primary mt-6"
              onClick={handleChooseFiles}
            >
              Choose Files
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".jpg,.jpeg,.png"
              onChange={handleFileInputChange}
              className="hidden"
            />
          </div>
        ) : (
          <div className="border-2 border-solid border-azure-300 rounded-lg p-8 bg-azure-50">
            <div className="text-6xl text-azure-500 mb-4">✅</div>
            <p className="text-lg font-medium text-neutral-700 mb-2">
              File Ready for Upload
            </p>
            <div className="bg-white rounded-lg p-4 mb-4">
              <p className="font-medium text-neutral-800">
                {selectedFile.name}
              </p>
              <p className="text-neutral-600">
                {formatFileSize(selectedFile.size)} •{" "}
                {selectedFile.type.split("/")[1].toUpperCase()}
              </p>
            </div>
            <div className="flex gap-4 justify-center">
              <button
                className="azure-button-secondary"
                onClick={handleRemoveFile}
                disabled={isUploading}
              >
                Remove File
              </button>
              <button
                className="azure-button-primary"
                onClick={handleUpload}
                disabled={isUploading || !token}
              >
                {isUploading ? "Uploading..." : "Upload to Azure"}
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}
      </div>
    </div>
  );
};
