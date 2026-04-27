function ResumeUpload({ setFiles }) {
    return (
      <div className="card">
        <h2>2. Upload Resume PDFs</h2>
  
        <input
          type="file"
          accept="application/pdf"
          multiple
          onChange={(e) => setFiles(Array.from(e.target.files))}
        />
      </div>
    );
  }
  
  export default ResumeUpload;