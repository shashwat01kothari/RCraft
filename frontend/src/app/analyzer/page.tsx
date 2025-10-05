"use client";

import { useState } from 'react';
import AnalyzerFileUploader from '../components/analyzer/AnalyzerFileUploader';
import FilePreview from '../components/analyzer/FilePreview';
import AnalyzerHeader from '../components/analyzer/AnalyzerHeader';
import FileInsight from '../components/analyzer/FileInsight';

const placeholderInsights = [
  { type: 'positive' as const, text: 'Strong Action Verbs', suggestion: 'Your document effectively uses impactful action verbs.' },
  { type: 'negative' as const, text: 'Formatting Issues Detected', suggestion: 'Complex tables or columns might not be parsed correctly by all systems.' },
  { type: 'neutral' as const, text: 'Keyword Optimization', suggestion: 'Consider adding keywords like "Project Management" and "Agile".' },
  { type: 'positive' as const, text: 'Clear Contact Information', suggestion: 'Contact details are easy to find and parse.' },
  { type: 'negative' as const, text: 'Repetitive Phrasing', suggestion: 'The phrase "responsible for" is used multiple times. Consider diversifying your language.' },
  { type: 'neutral' as const, text: 'Document Length', suggestion: 'The document is a single page, which is ideal for most applications.' },
];

const AnalyzerPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [showAnalysisView, setShowAnalysisView] = useState(false);

  const handleFileSelect = (selectedFile: File) => { setFile(selectedFile); setShowAnalysisView(false); };
  const handleAnalyzeClick = () => { if (file) { setShowAnalysisView(true); } else { alert("Please upload a file first."); } };
  const handleUploadNew = () => { setShowAnalysisView(false); setFile(null); };

  return (
    <main className="flex-grow bg-white w-full px-4 py-8">
      {!showAnalysisView ? (
        <div className="container mx-auto max-w-3xl">
          <AnalyzerFileUploader file={file} onFileSelect={handleFileSelect} />
          <div className="mt-8 text-center"><button onClick={handleAnalyzeClick} disabled={!file} className={`w-full md:w-auto px-12 py-3 bg-blue-500 text-white font-bold rounded-lg transition-all duration-300 shadow-sm ${!file ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'}`}>Analyze</button></div>
        </div>
      ) : (
        <div className="container mx-auto max-w-7xl">
          <div className="flex flex-col md:flex-row gap-8 items-start">
            
            {/* --- Left Column --- */}
            {/* CHANGE: This card now has a fixed height matching the right panel and overflow-hidden to contain the scrolling area. */}
            <div className="w-full md:w-1/2 flex flex-col bg-white border border-gray-200 rounded-lg shadow-sm h-[75vh] overflow-hidden">
              
              {/* This is the fixed header part. It will not scroll. */}
              {file && <AnalyzerHeader fileName={file.name} onUploadNew={handleUploadNew} />}

              {/* CHANGE: This new div wraps the content that needs to scroll. */}
              <div className="flex-grow overflow-y-auto">
                {/* The FileInsight component is placed inside the scrollable area. */}
                <FileInsight score={88} insights={placeholderInsights} />
              </div>
            </div>

            {/* --- Right Column (File Preview) --- */}
            <div className="w-full md:w-1/2 h-[75vh]">
              {file && <FilePreview file={file} />}
            </div>
          </div>
        </div>
      )}
    </main>
  );
};

export default AnalyzerPage;
