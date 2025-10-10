"use client";

import { PencilIcon, CheckIcon } from '@heroicons/react/24/solid';

interface JobDetails {
  companyName: string;
  jobRole: string;
  jobDescription: string;
}

interface JobDetailsFormProps {
  details: JobDetails;
  editingField: keyof JobDetails | null;
  onSetEditingField: (field: keyof JobDetails | null) => void;
  onDetailChange: (field: keyof JobDetails, value: string) => void;
  onSave: () => void;
}

const DetailRow = ({
  label,
  field,
  value,
  isEditing,
  onSetEditingField,
  onDetailChange,
  onSave,
}: {
  label: string;
  field: keyof JobDetails;
  value: string;
  isEditing: boolean;
  onSetEditingField: (field: keyof JobDetails | null) => void;
  onDetailChange: (field: keyof JobDetails, value: string) => void;
  onSave: () => void;
}) => {
  const isTextArea = field === 'jobDescription';
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !isTextArea) {
      onSave();
    }
    if (e.key === 'Escape') {
      onSetEditingField(null);
    }
  };
  return (
    <div className="p-4 border-b border-gray-200 last:border-b-0">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-sm font-medium text-gray-500">{label}</h3>
        <button 
          onClick={() => isEditing ? onSave() : onSetEditingField(field)}
          className="p-1 rounded-md hover:bg-gray-200 transition-colors"
          aria-label={isEditing ? `Save ${label}` : `Edit ${label}`}
        >
          {isEditing ? <CheckIcon className="h-4 w-4 text-green-600" /> : <PencilIcon className="h-4 w-4 text-gray-600" />}
        </button>
      </div>
      {isEditing ? (
        isTextArea ? (
          <textarea value={value} onChange={(e) => onDetailChange(field, e.target.value)} onKeyDown={handleKeyDown} className="w-full p-2 border border-blue-400 rounded-md text-gray-800 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" rows={5} autoFocus />
        ) : (
          <input type="text" value={value} onChange={(e) => onDetailChange(field, e.target.value)} onKeyDown={handleKeyDown} className="w-full p-2 border border-blue-400 rounded-md text-gray-800 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" autoFocus />
        )
      ) : (
        <p className="text-gray-800 whitespace-pre-wrap">{value}</p>
      )}
    </div>
  );
};

const JobDetailsForm = ({ details, editingField, onSetEditingField, onDetailChange, onSave }: JobDetailsFormProps) => {
  return (
    <div className="w-full h-full">
      {/* CHANGE: The header was removed from here. */}
      {/* The card now takes up the full height of its container. */}
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden h-full flex flex-col">
        <DetailRow 
          label="Company Name"
          field="companyName"
          value={details.companyName}
          isEditing={editingField === 'companyName'}
          onSetEditingField={onSetEditingField}
          onDetailChange={onDetailChange}
          onSave={onSave}
        />
        <DetailRow 
          label="Job Role"
          field="jobRole"
          value={details.jobRole}
          isEditing={editingField === 'jobRole'}
          onSetEditingField={onSetEditingField}
          onDetailChange={onDetailChange}
          onSave={onSave}
        />
        {/* Added flex-grow to the wrapper around the Job Description to make it fill remaining space */}
        <div className="flex-grow flex flex-col">
          <DetailRow 
            label="Job Description"
            field="jobDescription"
            value={details.jobDescription}
            isEditing={editingField === 'jobDescription'}
            onSetEditingField={onSetEditingField}
            onDetailChange={onDetailChange}
            onSave={onSave}
          />
        </div>
      </div>
    </div>
  );
};

export default JobDetailsForm;