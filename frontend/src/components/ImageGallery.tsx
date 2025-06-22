import React, { useState, useEffect } from "react";
import { imageService, type UserImage } from "../services/imageService";
import { useAuth } from "../hooks/useAuth";

export const ImageGallery: React.FC = () => {
  const [images, setImages] = useState<UserImage[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const { token } = useAuth();

  useEffect(() => {
    const fetchImages = async () => {
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        setError("");
        const userImages = await imageService.getUserImages(token);
        setImages(userImages);
      } catch (error) {
        console.error("Failed to fetch images:", error);
        setError(
          error instanceof Error ? error.message : "Failed to load images"
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchImages();
  }, [token]);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="azure-card p-8">
          <h2 className="text-2xl font-bold text-neutral-900 mb-4">
            My Image Gallery
          </h2>
          <p className="text-neutral-600 mb-8">
            Your uploaded images stored in Azure Blob Storage
          </p>
          <div className="text-center py-12">
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-8 w-8 text-azure-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Loading your images...
            </span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="azure-card p-8">
          <h2 className="text-2xl font-bold text-neutral-900 mb-4">
            My Image Gallery
          </h2>
          <p className="text-neutral-600 mb-8">
            Your uploaded images stored in Azure Blob Storage
          </p>
          <div className="text-center py-12">
            <div className="text-6xl text-red-400 mb-4">❌</div>
            <p className="text-red-600">{error}</p>
            <button
              className="azure-button-primary mt-4"
              onClick={() => window.location.reload()}
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="azure-card p-8">
        <h2 className="text-2xl font-bold text-neutral-900 mb-4">
          My Image Gallery
        </h2>
        <p className="text-neutral-600 mb-8">
          Your uploaded images stored in Azure Blob Storage ({images.length}{" "}
          image{images.length !== 1 ? "s" : ""})
        </p>

        {images.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl text-neutral-400 mb-4">🖼️</div>
            <p className="text-neutral-500 text-lg">No images uploaded yet</p>
            <p className="text-neutral-400 text-sm mt-2">
              Upload your first image to get started
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {images.map((image) => (
              <div
                key={image.id}
                className="azure-card overflow-hidden group hover:shadow-lg transition-shadow"
              >
                <div className="relative bg-neutral-100">
                  <img
                    src={image.blob_url}
                    alt={image.original_filename}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-200"
                    loading="lazy"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.src =
                        "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDMwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0xNTAgMTAwTDEyNSA3NUgxNzVMMTUwIDEwMFoiIGZpbGw9IiM5Q0EzQUYiLz4KPHN2ZyBkZW49IkltYWdlIG5vdCBhdmFpbGFibGUiIGZpbGw9IiM2QjcyODAiIGZvbnQtc2l6ZT0iMTQiIHRleHQtYW5jaG9yPSJtaWRkbGUiIHg9IjE1MCIgeT0iMTMwIj5JbWFnZSBub3QgYXZhaWxhYmxlPC90ZXh0Pgo8L3N2Zz4K";
                    }}
                  />
                  {image.upload_status === "processing" && (
                    <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                      <div className="text-white text-sm font-medium">
                        Processing...
                      </div>
                    </div>
                  )}
                  {image.upload_status === "failed" && (
                    <div className="absolute inset-0 bg-red-500 bg-opacity-75 flex items-center justify-center">
                      <div className="text-white text-sm font-medium">
                        Failed
                      </div>
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3
                    className="font-medium text-neutral-900 truncate"
                    title={image.original_filename}
                  >
                    {image.original_filename}
                  </h3>
                  <div className="text-sm text-neutral-500 mt-1 space-y-1">
                    <div className="flex justify-between">
                      <span>
                        {image.width} × {image.height}
                      </span>
                      <span>
                        {formatFileSize(
                          image.processed_size || image.file_size
                        )}
                      </span>
                    </div>
                    <div className="text-xs text-neutral-400">
                      {formatDate(image.created_at)}
                    </div>
                    <div className="flex items-center gap-2">
                      <span
                        className={`inline-block w-2 h-2 rounded-full ${
                          image.upload_status === "completed"
                            ? "bg-green-500"
                            : image.upload_status === "processing"
                            ? "bg-yellow-500"
                            : "bg-red-500"
                        }`}
                      />
                      <span className="text-xs capitalize">
                        {image.upload_status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
