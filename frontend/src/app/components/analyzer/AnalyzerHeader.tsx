"use client";

import { DocumentIcon } from '@heroicons/react/24/solid';

interface AnalyzerHeaderProps {
  fileName: string;
  onUploadNew: () => void;
}

const AnalyzerHeader = ({ fileName, onUploadNew }: AnalyzerHeaderProps) => {
  return (
    // CHANGE: Removed card styles (bg, border, rounded). Added a bottom border separator.
    <div className="w-full flex items-center justify-between p-3 border-b border-gray-200">
      {/* File name display */}
      <div className="flex items-center">
        <div className="flex items-center px-3 py-1.5 bg-white border border-gray-300 rounded-md shadow-sm">
          <DocumentIcon className="h-5 w-5 text-gray-500 mr-2" />
          <span className="text-sm font-medium text-gray-800 truncate">
            {fileName}
          </span>
        </div>
      </div>

      {/* Upload New button */}
      <button
        onClick={onUploadNew}
        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md transition duration-300 text-sm shadow-sm"
      >
        Upload New
      </button>
    </div>
  );
};

export default AnalyzerHeader;