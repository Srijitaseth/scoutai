import RealAgentChat from "./RealAgentChat";

function CandidatePortal({ selectedCandidate, onCandidateUpdate, onRankUpdate }) {
  if (!selectedCandidate) {
    return (
      <div className="card">
        <h2>Candidate Portal</h2>
        <p>No candidate selected yet. Please analyze candidates from the recruiter portal first.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="card candidate-hero">
        <h2>Candidate Portal</h2>
        <p>
          Welcome, <b>{selectedCandidate.name}</b>. ScoutAI will ask a few quick
          questions to understand your genuine interest in the role.
        </p>

        <div className="candidate-summary">
          <p><b>Email:</b> {selectedCandidate.email}</p>
          <p><b>Match Score:</b> {selectedCandidate.match_score}</p>
          <p><b>Current Interest Score:</b> {selectedCandidate.interest_score}</p>
          <p><b>Final Score:</b> {selectedCandidate.final_score}</p>
        </div>
      </div>

      <div className="card">
        <RealAgentChat
          candidate={selectedCandidate}
          onCandidateUpdate={onCandidateUpdate}
          onRankUpdate={onRankUpdate}
        />
      </div>
    </div>
  );
}

export default CandidatePortal;