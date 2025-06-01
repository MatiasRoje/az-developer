import React, { useState } from "react";
import { ImageUpload } from "../components/ImageUpload";
import { ImageGallery } from "../components/ImageGallery";

type TabType = "upload" | "gallery";

export const DashboardPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>("upload");

  return (
    <section>
      <div className="container mx-auto px-4">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab("upload")}
            className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === "upload"
                ? "border-azure-500 text-azure-600"
                : "border-transparent text-neutral-500 hover:text-neutral-700"
            }`}
          >
            Upload Images
          </button>
          <button
            onClick={() => setActiveTab("gallery")}
            className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
              activeTab === "gallery"
                ? "border-azure-500 text-azure-600"
                : "border-transparent text-neutral-500 hover:text-neutral-700"
            }`}
          >
            My Gallery
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      <div className="container mx-auto px-4 py-8">
        {activeTab === "upload" ? <ImageUpload /> : <ImageGallery />}
      </div>
    </section>
  );
};
