"use client";

import { CheckCircleIcon, XCircleIcon, LightBulbIcon } from '@heroicons/react/24/outline';

// --- Data Structures (for production-grade props) ---
interface Insight {
  type: 'positive' | 'negative' | 'neutral';
  text: string;
  suggestion: string;
}

interface FileInsightProps {
  score: number;
  insights: Insight[];
}

// --- Helper Component (Declared once, correctly) ---
const InsightItem = ({ insight }: { insight: Insight }) => {
  const iconMap = {
    positive: <CheckCircleIcon className="h-6 w-6 text-green-500" />,
    negative: <XCircleIcon className="h-6 w-6 text-red-500" />,
    neutral: <LightBulbIcon className="h-6 w-6 text-yellow-500" />,
  };

  return (
    <div className="flex items-start gap-3">
      <div className="flex-shrink-0 mt-0.5">{iconMap[insight.type]}</div>
      <div>
        <p className="font-semibold text-gray-800">{insight.text}</p>
        <p className="text-sm text-gray-600">{insight.suggestion}</p>
      </div>
    </div>
  );
};

// --- Main Component ---
const FileInsight = ({ score, insights }: FileInsightProps) => {
  return (
    // Main container is now just a wrapper
    <div>
      {/* --- 1. Scoring Div --- */}
      <div className="p-6 text-center border-b border-gray-200">
        <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">
          Overall Score
        </h3>
        <p className="text-7xl font-bold text-blue-600 my-2">
          {score}
        </p>
        <p className="text-sm text-gray-500">
          This score reflects your document's compatibility and clarity.
        </p>
      </div>

      {/* --- 2. Analysis Div --- */}
      <div className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Key Insights
        </h3>
        <div className="flex flex-col gap-5">
          {insights.map((insight, index) => (
            <InsightItem key={index} insight={insight} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default FileInsight;