"use client";

import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { DocumentArrowUpIcon } from '@heroicons/react/24/outline';

interface OptimizerFileUploaderProps {
  file: File | null;
  onFileSelect: (file: File) => void;
}

const OptimizerFileUploader = ({ file, onFileSelect }: OptimizerFileUploaderProps) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setIsDragOver(true); };
  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setIsDragOver(false); };
  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (files && files.length > 0) onFileSelect(files[0]);
  };
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) onFileSelect(files[0]);
  };
  const handleBrowseClick = () => { fileInputRef.current?.click(); };
  
  // NEW: Handler for the "Build from scratch" button
  const handleBuildFromScratch = () => {
    console.log("User wants to build a resume from scratch.");
    alert("Resume builder functionality is not yet implemented.");
  };

  return (
    // This wrapper div allows us to add the button below the dropzone
    <div>
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`w-full p-8 border-2 border-dashed rounded-lg transition-colors duration-300 h-full flex flex-col justify-center
          ${isDragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}`}
      >
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="p-4 bg-gray-100 rounded-full">
            <DocumentArrowUpIcon className="w-10 h-10 text-gray-500" />
          </div>
          {file ? (
            <p className="text-lg font-semibold text-gray-800">{file.name}</p>
          ) : (
            <div>
              <p className="text-lg font-semibold text-gray-700">
                <button onClick={handleBrowseClick} className="text-blue-500 font-bold hover:underline">
                  Upload Resume
                </button>
                {' '}or drag and drop
              </p>
              <p className="text-sm text-gray-500 mt-1">PDF, DOC, or DOCX</p>
            </div>
          )}
          <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" accept=".pdf,.doc,.docx" />
        </div>
      </div>
      
      {/* NEW: "Build from scratch" button section */}
      <div className="text-center mt-4">
        <button 
          onClick={handleBuildFromScratch}
          className="text-sm text-gray-500 underline hover:text-gray-800 transition-colors"
        >
          Build a resume from scratch
        </button>
      </div>
    </div>
  );
};

export default OptimizerFileUploader;