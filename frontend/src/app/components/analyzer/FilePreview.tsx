"use client";

import { useState, useEffect } from 'react';
// Import the refresh icon
import { DocumentIcon, ExclamationTriangleIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

interface FilePreviewProps {
  file: File;
}

const FilePreview = ({ file }: FilePreviewProps) => {
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  // NEW: State to act as a key for re-rendering the iframe
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const url = URL.createObjectURL(file);
    setFileUrl(url);
    // When a new file is uploaded, reset the refresh key
    setRefreshKey(0);

    // Cleanup function to prevent memory leaks
    return () => {
      URL.revokeObjectURL(url);
      setFileUrl(null);
    };
  }, [file]); // Effect re-runs only when the file prop itself changes

  // NEW: Handler to increment the key, forcing a re-render
  const handleRefresh = () => {
    setRefreshKey(prevKey => prevKey + 1);
  };

  const renderPreview = () => {
    if (!fileUrl) {
      return null; // Or a loading spinner
    }

    if (file.type === 'application/pdf') {
      return (
        <iframe
          // The key prop is the magic here. When it changes, the iframe is recreated.
          key={refreshKey}
          src={fileUrl}
          className="w-full h-full"
          title="File Preview"
        />
      );
    }

    return (
      <div key={refreshKey} className="flex flex-col items-center justify-center h-full bg-gray-50 text-center p-4">
        <ExclamationTriangleIcon className="w-12 h-12 text-yellow-500 mb-4" />
        <h3 className="font-bold text-gray-800">Preview not available</h3>
        <p className="text-sm text-gray-500">
          Your browser does not support previews for <strong>.{file.name.split('.').pop()}</strong> files.
        </p>
      </div>
    );
  };

  return (
    <div className="w-full h-full bg-white rounded-lg border border-gray-200 shadow-sm flex flex-col overflow-hidden">
      {/* --- Header of the preview panel --- */}
      {/* CHANGE: Updated the header to a flex container with space-between */}
      <div className="flex items-center justify-between p-3 border-b border-gray-200 bg-gray-50/50">
        {/* Left side: Icon and filename */}
        <div className="flex items-center min-w-0"> {/* min-w-0 is a trick to help truncation work in flexbox */}
          <DocumentIcon className="h-5 w-5 text-gray-500 mr-2 flex-shrink-0" />
          <span className="font-semibold text-gray-800 text-sm truncate">{file.name}</span>
        </div>

        {/* Right side: Refresh button */}
        <div>
          <button
            onClick={handleRefresh}
            className="p-1 rounded-md hover:bg-gray-200 transition-colors"
            aria-label="Refresh Preview"
          >
            <ArrowPathIcon className="h-5 w-5 text-gray-600" />
          </button>
        </div>
      </div>
      
      {/* The actual preview area */}
      <div className="flex-grow">
        {renderPreview()}
      </div>
    </div>
  );
};

export default FilePreview;