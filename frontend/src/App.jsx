import { useState } from "react";
import UploadBox from "./components/UploadBox";
import QueryBox from "./components/QueryBox";
import AnswerBox from "./components/AnswerBox";
import { Sparkles, AlertCircle } from 'lucide-react';
import "./App.css";

export default function App() {
  const [answer, setAnswer] = useState("");

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100">
      {/* Subtle background pattern */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-30">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-200 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-200 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-500 rounded-xl shadow-lg">
              <Sparkles className="w-7 h-7 text-white" />
            </div>
            <h1 className="text-5xl font-bold text-slate-800">
              Smart Compliance Assistant
            </h1>
          </div>
          <p className="text-slate-600 text-lg">
            Upload documents and get instant compliance insights powered by AI
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-6">
          <UploadBox />
          <QueryBox setAnswer={setAnswer} />
        </div>

        {/* Answer Section */}
        <div className="mt-6">
          <AnswerBox answer={answer} />
        </div>

        {/* Footer Info */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full border border-slate-200 shadow-sm">
            <AlertCircle className="w-4 h-4 text-blue-500" />
            <p className="text-sm text-slate-600">
              Your documents are processed securely and privately
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
