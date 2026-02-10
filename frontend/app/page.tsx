'use client';

import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-mesh flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Blobs */}
      <div className="absolute top-0 -left-4 w-72 h-72 bg-primary-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
      <div className="absolute top-0 -right-4 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
      <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>

      <div className="max-w-2xl w-full z-10">
        <div className="card-glass p-12 md:p-16 text-center space-y-10">
          <div className="space-y-4">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary-50 text-primary-700 text-sm font-bold tracking-wide uppercase shadow-sm border border-primary-100 mb-6 animate-pulse">
              🚀 Version 2.0 is live
            </div>

            <h1 className="text-5xl md:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Manage Tasks with <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-indigo-600">Maxim</span>
            </h1>

            <p className="text-xl text-slate-600 max-w-lg mx-auto leading-relaxed">
              Experience the next generation of task management. Beautiful, fast, and engineered for peak productivity.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link
              href="/auth/login"
              className="btn-primary flex items-center justify-center py-4 px-10 text-lg group"
            >
              Get Started
              <svg
                className="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <Link
              href="/auth/register"
              className="btn-secondary flex items-center justify-center py-4 px-10 text-lg border border-slate-200 shadow-sm"
            >
              Create Account
            </Link>
          </div>

          <div className="pt-10 border-t border-slate-100">
            <div className="flex flex-col items-center space-y-4">
              <p className="text-sm font-semibold text-slate-400 uppercase tracking-[0.2em]">Designed & Crafted By</p>
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary-600 to-indigo-600 flex items-center justify-center text-white font-bold shadow-lg shadow-primary-500/30">
                  WG
                </div>
                <span className="text-lg font-bold text-slate-800">Waseem Ghazi</span>
              </div>
            </div>
          </div>
        </div>

        {/* Floating Feature Pills */}
        <div className="mt-12 flex flex-wrap justify-center gap-4 animate-fade-in">
          {['Lightning Fast', 'Cloud Sync', 'Secure SSL', 'Modern UI'].map((feature) => (
            <div
              key={feature}
              className="px-6 py-2 bg-white/50 backdrop-blur-md rounded-full text-sm font-semibold text-slate-600 border border-white shadow-sm"
            >
              {feature}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}