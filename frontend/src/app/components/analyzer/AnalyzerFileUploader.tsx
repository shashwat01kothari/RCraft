"use client";

import { useRef, DragEvent, ChangeEvent, useState } from 'react';
import { DocumentArrowUpIcon } from '@heroicons/react/24/outline';

interface AnalyzerFileUploaderProps {
  file: File | null;
  onFileSelect: (file: File) => void;
  // REMOVED: The isMinimized prop is no longer needed
}

const AnalyzerFileUploader = ({ file, onFileSelect }: AnalyzerFileUploaderProps) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // --- Event handlers remain the same ---
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setIsDragOver(true); };
  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setIsDragOver(false); };
  const handleDrop = (e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setIsDragOver(false); const f = e.dataTransfer.files; if(f && f.length > 0) onFileSelect(f[0]); };
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => { const f = e.target.files; if(f && f.length > 0) onFileSelect(f[0]); };
  const handleSelectFileClick = () => { fileInputRef.current?.click(); };

  return (
    // REMOVED: The conditional rendering logic is gone. This component now only has one state.
    <div className="w-full text-center">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
        Analyze and Score your Resume
      </h1>
      <p className="text-lg text-gray-500 mb-10">
        Upload your document below to get an instant analysis and score.
      </p>

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`w-full p-8 border-2 border-dashed rounded-lg transition-colors duration-300 ${isDragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}`}
      >
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="p-4 bg-gray-100 rounded-full">
            <DocumentArrowUpIcon className="w-10 h-10 text-gray-500" />
          </div>
          {file ? ( <p className="text-lg font-semibold text-gray-800">{file.name}</p> ) : ( <div> <p className="text-lg font-semibold text-gray-700"> <button onClick={handleSelectFileClick} className="text-blue-500 font-bold hover:underline"> Click to upload </button> {' '}or drag and drop </p> <p className="text-sm text-gray-500 mt-1">PDF, DOC, or DOCX</p> </div> )}
          <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" accept=".pdf,.doc,.docx" />
        </div>
      </div>
    </div>
  );
};

export default AnalyzerFileUploader;