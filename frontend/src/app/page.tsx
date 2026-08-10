"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { Briefcase, MapPin, Building2, Search, Sparkles } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  salary?: string;
  job_type: string;
  created_at: string;
}

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const res = await axios.get(`${API_URL}/jobs`);
      setJobs(res.data);
    } catch (err) {
      console.error("Failed to fetch jobs", err);
      // Demo data if backend is not running
      setJobs([
        {
          id: 1,
          title: "Senior Full Stack Developer",
          company: "Sirmint Technology",
          location: "Remote / India",
          description: "Build modern web applications using React, Next.js and ASP.NET Core. Experience with cloud and AI preferred.",
          salary: "₹15-25 LPA",
          job_type: "Full-time",
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          title: "AI Engineer",
          company: "Orlina AI",
          location: "Bangalore",
          description: "Work on cutting-edge AI products, LLM integrations and production AI systems.",
          salary: "₹20-35 LPA",
          job_type: "Full-time",
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          title: "Frontend Developer (React)",
          company: "DealNavo",
          location: "Mumbai",
          description: "Create beautiful, responsive e-commerce experiences with React and Tailwind.",
          salary: "₹10-18 LPA",
          job_type: "Full-time",
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const filteredJobs = jobs.filter(
    (job) =>
      job.title.toLowerCase().includes(search.toLowerCase()) ||
      job.company.toLowerCase().includes(search.toLowerCase()) ||
      job.location.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Navbar */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
              <Briefcase className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl text-slate-800">AI Job Portal</span>
          </div>
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-blue-600 transition">
              Login
            </button>
            <button className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-xl transition shadow-lg shadow-blue-500/20">
              Post a Job
            </button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-4 pt-16 pb-12 text-center">
        <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-1.5 rounded-full text-sm font-medium mb-6">
          <Sparkles className="w-4 h-4" />
          AI-Powered Job Matching
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4 leading-tight">
          Find Your Dream Job with <span className="text-blue-600">AI</span>
        </h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto mb-8">
          Smart matching between candidates and opportunities. Upload your resume and let AI find the best roles for you.
        </p>

        {/* Search */}
        <div className="max-w-2xl mx-auto relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search jobs, companies, locations..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-12 pr-4 py-4 rounded-2xl border border-slate-200 shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-slate-800"
          />
        </div>
      </section>

      {/* Jobs List */}
      <section className="max-w-6xl mx-auto px-4 pb-20">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-slate-800">
            {loading ? "Loading..." : `${filteredJobs.length} Jobs Found`}
          </h2>
        </div>

        {loading ? (
          <div className="grid gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-2xl p-6 shadow-sm animate-pulse h-40" />
            ))}
          </div>
        ) : (
          <div className="grid gap-4">
            {filteredJobs.map((job) => (
              <div
                key={job.id}
                className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition border border-slate-100 hover:border-blue-100"
              >
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-slate-900 mb-1">{job.title}</h3>
                    <div className="flex flex-wrap items-center gap-3 text-sm text-slate-500 mb-3">
                      <span className="flex items-center gap-1">
                        <Building2 className="w-4 h-4" />
                        {job.company}
                      </span>
                      <span className="flex items-center gap-1">
                        <MapPin className="w-4 h-4" />
                        {job.location}
                      </span>
                      <span className="bg-blue-50 text-blue-700 px-2.5 py-0.5 rounded-full text-xs font-medium">
                        {job.job_type}
                      </span>
                    </div>
                    <p className="text-slate-600 text-sm line-clamp-2">{job.description}</p>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    {job.salary && (
                      <span className="text-green-600 font-semibold">{job.salary}</span>
                    )}
                    <button className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-xl transition">
                      Apply Now
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white/50 py-8">
        <div className="max-w-6xl mx-auto px-4 text-center text-sm text-slate-500">
          <p>
            Built by <strong>Rajiv Kapur</strong> · Software Architect & Full Stack Developer
          </p>
          <p className="mt-1">AI Job Portal · Portfolio Project</p>
        </div>
      </footer>
    </div>
  );
}
