"use client";

import { useState } from 'react';
import JobDetailsForm from '../components/optimizer/JobDetailsForm';
import OptimizerFileUploader from '../components/optimizer/OptimizerFileUploader';

interface JobDetails { companyName: string; jobRole: string; jobDescription: string; }

const initialDetails: JobDetails = {
  companyName: "Tech Solutions Inc.",
  jobRole: "Senior Frontend Developer",
  jobDescription: "Developing and maintaining web applications...",
};

const OptimizerPage = () => {
  const [jobDetails, setJobDetails] = useState<JobDetails>(initialDetails);
  const [file, setFile] = useState<File | null>(null);
  const [editingField, setEditingField] = useState<keyof JobDetails | null>(null);

  const handleFileSelect = (selectedFile: File) => { setFile(selectedFile); };
  const handleDetailChange = (field: keyof JobDetails, value: string) => { setJobDetails(prev => ({ ...prev, [field]: value })); };
  const handleSaveDetail = () => { setEditingField(null); };
  const handleOptimizeClick = () => { alert("Optimization functionality is not yet implemented."); };

  return (
    <main className="flex-grow bg-gray-50 w-full px-4 py-12">
      <div className="container mx-auto max-w-6xl">

        <div className="text-center mb-12">
          {/* CHANGE (a): Increased font size */}
          <h1 className="text-6xl font-bold text-gray-800">
            Optimize your Resume
          </h1>
          <p className="mt-4 text-xl text-gray-600">
            Tailor your Resume for any particular Job
          </p>
        </div>

        {/* This flex container no longer needs a fixed height. It will grow with its content. */}
        <div className="flex flex-col md:flex-row gap-8 items-stretch">
          
          {/* Left Column (50% width) */}
          <div className="w-full md:w-1/2">
            <JobDetailsForm 
              details={jobDetails}
              editingField={editingField}
              onSetEditingField={setEditingField}
              onDetailChange={handleDetailChange}
              onSave={handleSaveDetail}
            />
          </div>

          {/* Right Column (50% width) */}
          {/* CHANGE (c): This structure ensures the button is positioned correctly */}
          <div className="w-full md:w-1/2 flex flex-col gap-4">
            <div className="flex-grow">
              <OptimizerFileUploader 
                file={file}
                onFileSelect={handleFileSelect}
              />
            </div>
            
            <div className="flex justify-center">
              {/* CHANGE (d): Made button smaller and centered */}
              <button
                onClick={handleOptimizeClick}
                className={`w-auto px-12 py-3 bg-blue-500 text-white font-bold rounded-lg transition-all duration-300 shadow-sm hover:bg-blue-600`}
              >
                Optimize Resume
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default OptimizerPage;