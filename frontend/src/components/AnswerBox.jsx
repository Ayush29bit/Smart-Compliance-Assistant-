import { CheckCircle } from 'lucide-react';

export default function AnswerBox({ answer }) {
  if (!answer) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-lg animate-in fade-in duration-500">
      <div className="flex items-start gap-4">
        <div className="p-2 bg-green-50 rounded-lg flex-shrink-0">
          <CheckCircle className="w-6 h-6 text-green-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-slate-800 mb-3">
            Assistant Response
          </h3>
          <div className="prose max-w-none">
            <p className="text-slate-600 leading-relaxed">{answer}</p>
          </div>
        </div>
      </div>
    </div>
  );
}