import React from "react";

export const ImageGallery: React.FC = () => {
  // Mock data for now
  const mockImages = [
    { id: "1", url: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop", name: "Mountain Landscape" },
    { id: "2", url: "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=300&h=200&fit=crop", name: "Ocean View" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="azure-card p-8">
        <h2 className="text-2xl font-bold text-neutral-900 mb-4">My Image Gallery</h2>
        <p className="text-neutral-600 mb-8">
          Your uploaded images stored in Azure Blob Storage
        </p>
        
        {mockImages.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl text-neutral-400 mb-4">🖼️</div>
            <p className="text-neutral-500">No images uploaded yet</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockImages.map((image) => (
              <div key={image.id} className="azure-card overflow-hidden">
                <img
                  src={image.url}
                  alt={image.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-4">
                  <h3 className="font-medium text-neutral-900">{image.name}</h3>
                  <p className="text-sm text-neutral-500 mt-1">
                    Uploaded today
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}; 