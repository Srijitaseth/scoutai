import { useState } from "react";
import { analyzeResumes } from "./api";
import JDInput from "./components/JDInput";
import ResumeUpload from "./components/ResumeUpload";
import CandidateTable from "./components/CandidateTable";
import CandidateDetails from "./components/CandidateDetails";
import DashboardCharts from "./components/DashboardCharts";
import ExportButtons from "./components/ExportButtons";
import CandidatePortal from "./components/CandidatePortal";
import "./index.css";

function App() {
  const [activePortal, setActivePortal] = useState("recruiter");

  const [jdText, setJdText] = useState("");
  const [files, setFiles] = useState([]);
  const [parsedJd, setParsedJd] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    if (!jdText || files.length === 0) {
      alert("Please enter JD and upload resume PDFs.");
      return;
    }

    setLoading(true);

    const data = await analyzeResumes(jdText, files);

    setParsedJd(data.parsed_jd);
    setCandidates(data.ranked_candidates);
    setSelectedCandidate(data.ranked_candidates[0]);

    setLoading(false);
  }

  function handleFeedbackUpdate(feedbackType) {
    const updatedCandidates = candidates.map((candidate) => {
      if (candidate.id === selectedCandidate.id) {
        return {
          ...candidate,
          recruiter_feedback: feedbackType,
        };
      }

      return candidate;
    });

    const updatedSelectedCandidate = {
      ...selectedCandidate,
      recruiter_feedback: feedbackType,
    };

    setCandidates(updatedCandidates);
    setSelectedCandidate(updatedSelectedCandidate);
  }

  function handleCandidateUpdate(updatedCandidate) {
    const updatedCandidates = candidates.map((candidate) => {
      if (candidate.id === updatedCandidate.id) {
        return updatedCandidate;
      }

      return candidate;
    });

    setCandidates(updatedCandidates);
    setSelectedCandidate(updatedCandidate);
  }

  function handleRankUpdate(updatedRankedCandidates) {
    setCandidates(updatedRankedCandidates);

    const stillSelected = updatedRankedCandidates.find(
      (candidate) => candidate.id === selectedCandidate.id
    );

    if (stillSelected) {
      setSelectedCandidate(stillSelected);
    }
  }

  return (
    <div className="page">
      <div className="top-header">
        <div>
          <h1>ScoutAI</h1>
          <p className="subtitle">
            AI-Powered Talent Scouting & Engagement Agent
          </p>
        </div>

        <div className="portal-switch">
          <button
            className={activePortal === "recruiter" ? "active-tab" : ""}
            onClick={() => setActivePortal("recruiter")}
          >
            Recruiter Portal
          </button>

          <button
            className={activePortal === "candidate" ? "active-tab" : ""}
            onClick={() => setActivePortal("candidate")}
          >
            Candidate Portal
          </button>
        </div>
      </div>

      {activePortal === "recruiter" && (
        <>
          <div className="portal-note">
            <b>Recruiter Portal:</b> Paste the JD, upload resumes, analyze
            candidates, review scores, send outreach, give feedback, and export
            the shortlist.
          </div>

          <JDInput jdText={jdText} setJdText={setJdText} />

          <ResumeUpload setFiles={setFiles} />

          <button className="primary-btn" onClick={handleAnalyze}>
            {loading ? "Analyzing with AI..." : "Analyze Candidates"}
          </button>

          {parsedJd && (
            <div className="card">
              <h2>Parsed Job Description</h2>
              <p><b>Role:</b> {parsedJd.job_title}</p>
              <p><b>Must-Have Skills:</b> {parsedJd.must_have_skills?.join(", ")}</p>
              <p><b>Nice-to-Have Skills:</b> {parsedJd.nice_to_have_skills?.join(", ")}</p>
              <p><b>Experience:</b> {parsedJd.experience_required}</p>
              <p><b>Location:</b> {parsedJd.location}</p>
              <p><b>Work Mode:</b> {parsedJd.work_mode}</p>
              <p><b>Seniority:</b> {parsedJd.seniority}</p>

              <h3>Responsibilities</h3>
              <ul>
                {parsedJd.responsibilities?.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {candidates.length > 0 && (
            <>
              <CandidateTable
                candidates={candidates}
                setSelectedCandidate={setSelectedCandidate}
              />

              <CandidateDetails
                candidate={selectedCandidate}
                onFeedbackUpdate={handleFeedbackUpdate}
              />

              <DashboardCharts candidates={candidates} />

              <ExportButtons />
            </>
          )}
        </>
      )}

      {activePortal === "candidate" && (
        <>
          <div className="portal-note">
            <b>Candidate Portal:</b> This is the candidate-facing engagement
            experience. In production, this chat link would be sent to the
            candidate by email.
          </div>

          <CandidatePortal
            selectedCandidate={selectedCandidate}
            onCandidateUpdate={handleCandidateUpdate}
            onRankUpdate={handleRankUpdate}
          />
        </>
      )}
    </div>
  );
}

export default App;