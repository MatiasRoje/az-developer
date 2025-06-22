/**
 * Image Service for Azure Certification Demo
 * AZ-204 Focus: Blob Storage integration with async processing
 */

import type { AuthToken } from "../types/auth";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

export interface ImageUploadResponse {
  upload_id: string;
  message: string;
  status: "queued" | "processing" | "completed" | "failed";
}

export interface UserImage {
  id: string;
  filename: string;
  original_filename: string;
  blob_url: string;
  width?: number;
  height?: number;
  file_size: number;
  upload_status: "processing" | "completed" | "failed";
  created_at: string;
}

export interface UserImagesResponse {
  images: UserImage[];
  count: number;
}

class ImageServiceError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ImageServiceError";
  }
}

export class ImageService {
  private static instance: ImageService;

  static getInstance(): ImageService {
    if (!ImageService.instance) {
      ImageService.instance = new ImageService();
    }
    return ImageService.instance;
  }

  /**
   * Upload image file
   * AZ-204 Pattern: Async processing with queue system (RabbitMQ -> Service Bus)
   */
  async uploadImage(
    file: File,
    token: AuthToken
  ): Promise<ImageUploadResponse> {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/api/image-service/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token.access_token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: "Upload failed" }));
        throw new ImageServiceError(
          errorData.detail || `Upload failed: ${response.statusText}`,
          response.status
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ImageServiceError) {
        throw error;
      }
      throw new ImageServiceError("Network error: Unable to upload image");
    }
  }

  /**
   * Get user's images
   * AZ-204 Pattern: Blob Storage with SAS tokens
   */
  async getUserImages(token: AuthToken): Promise<UserImage[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/image-service/images`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token.access_token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: "Failed to fetch images" }));
        throw new ImageServiceError(
          errorData.detail || `Failed to fetch images: ${response.statusText}`,
          response.status
        );
      }

      const data: UserImagesResponse = await response.json();
      return data.images;
    } catch (error) {
      if (error instanceof ImageServiceError) {
        throw error;
      }
      throw new ImageServiceError("Network error: Unable to fetch images");
    }
  }

  /**
   * Get specific image details
   * AZ-204 Pattern: Direct HTTP for fast read operations
   */
  async getImage(imageId: string, token: AuthToken): Promise<UserImage> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/image-service/images/${imageId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token.access_token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new ImageServiceError(
          `Failed to get image: ${response.statusText}`,
          response.status
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ImageServiceError) {
        throw error;
      }
      throw new ImageServiceError("Network error: Unable to get image");
    }
  }
}

export const imageService = ImageService.getInstance();
