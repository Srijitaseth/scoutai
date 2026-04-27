function CandidateTable({ candidates, setSelectedCandidate }) {
    return (
      <div className="card">
        <h2>3. Ranked Candidate Shortlist</h2>
  
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Candidate</th>
              <th>Match</th>
              <th>Interest</th>
              <th>Final</th>
              <th>Action</th>
            </tr>
          </thead>
  
          <tbody>
            {candidates.map((candidate, index) => (
              <tr key={index} onClick={() => setSelectedCandidate(candidate)}>
                <td>{index + 1}</td>
                <td>{candidate.name}</td>
                <td>{candidate.match_score}</td>
                <td>{candidate.interest_score}</td>
                <td>{candidate.final_score}</td>
                <td>{candidate.recommended_action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  
  export default CandidateTable;