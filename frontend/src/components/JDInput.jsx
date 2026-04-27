function JDInput({ jdText, setJdText }) {
    return (
      <div className="card">
        <h2>1. Paste Job Description</h2>
  
        <textarea
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          placeholder="Paste the full job description here..."
          rows="8"
        />
      </div>
    );
  }
  
  export default JDInput;