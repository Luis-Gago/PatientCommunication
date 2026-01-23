'use client';

import React, { useState } from 'react';

interface PADImage {
  topic: string;
  filename: string;
}

const PAD_IMAGES: PADImage[] = [
  { topic: 'What is PAD', filename: 'PAD.jpg' },
  { topic: 'Atherosclerosis vs Normal Artery', filename: 'pad_1 from NIH.jpg' },
  { topic: 'Circulation System', filename: 'Circulation system.jpg' },
  { topic: 'Artery vs Vein', filename: 'Artery and vein.jpg' },
  { topic: 'Stages of PAD', filename: 'Stages of PAD.jpg' },
  { topic: 'Risk Factors for PAD', filename: 'Risk factors for PAD.jpg' },
  { topic: 'Complications of PAD', filename: 'Complications of PAD.jpg' },
  { topic: 'Pain in Legs When Walking', filename: 'pain in legs when walking.jpg' },
  { topic: 'Diagnostic Tests for PAD', filename: 'diagnostic tests for PAD.jpg' },
  { topic: 'Ankle Brachial Index (ABI)', filename: 'ankle-brachial index test_1 from NIH.jpg' },
  { topic: 'Medications for PAD', filename: 'Medications.jpg' },
  { topic: 'Lifestyle Changes for PAD', filename: 'lifestyle changes for PAD.jpg' },
  { topic: 'How Smoking Affects PAD', filename: 'how smoking affects PAD.jpg' },
  { topic: 'Foot Sores and Ulcers', filename: 'foot sores and ulcers copy.jpg' },
  { topic: 'Stenting of Leg Artery', filename: 'Stenting of a leg artery.jpg' },
];

const BASE_URL = 'https://raw.githubusercontent.com/DrDavidL/pad/main/images/';

interface ImageModalProps {
  image: PADImage | null;
  onClose: () => void;
}

function ImageModal({ image, onClose }: ImageModalProps) {
  if (!image) return null;

  const imageUrl = `${BASE_URL}${encodeURIComponent(image.filename)}`;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-start p-4 bg-black/70"
      onClick={onClose}
    >
      <div
        className="relative max-w-2xl max-h-[90vh] bg-white rounded-xl shadow-2xl overflow-hidden mt-4 ml-4"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
          <h3 className="text-lg font-semibold pr-8">{image.topic}</h3>
          <button
            onClick={onClose}
            className="absolute top-3 right-3 w-8 h-8 flex items-center justify-center bg-white/20 hover:bg-white/30 rounded-full transition-colors"
            aria-label="Close"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Image Container */}
        <div className="p-4 bg-gray-50">
          <img
            src={imageUrl}
            alt={image.topic}
            className="max-w-full max-h-[70vh] mx-auto rounded-lg shadow-lg object-contain"
          />
        </div>
      </div>
    </div>
  );
}

interface PADImageGalleryProps {
  collapsed?: boolean;
}

export default function PADImageGallery({ collapsed = true }: PADImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<PADImage | null>(null);
  const [isExpanded, setIsExpanded] = useState(!collapsed);

  return (
    <>
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
        {/* Gallery Header - Clickable to expand/collapse */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 transition-colors"
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl">🖼️</span>
            <div className="text-left">
              <h3 className="font-semibold text-gray-900">PAD Educational Images</h3>
              <p className="text-xs text-gray-600">Click to view helpful diagrams and illustrations</p>
            </div>
          </div>
          <svg
            className={`w-5 h-5 text-gray-500 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        {/* Image List */}
        {isExpanded && (
          <div className="p-3 max-h-64 overflow-y-auto">
            <div className="grid grid-cols-1 gap-2">
              {PAD_IMAGES.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(image)}
                  className="flex items-center gap-3 p-3 text-left bg-gray-50 hover:bg-purple-50 rounded-lg transition-colors group"
                >
                  <div className="flex-shrink-0 w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center group-hover:bg-purple-200 transition-colors">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <span className="text-sm font-medium text-gray-700 group-hover:text-purple-700">
                    {image.topic}
                  </span>
                  <svg className="w-4 h-4 ml-auto text-gray-400 group-hover:text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Modal for viewing selected image */}
      <ImageModal image={selectedImage} onClose={() => setSelectedImage(null)} />
    </>
  );
}
