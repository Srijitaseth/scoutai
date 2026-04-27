import { downloadCSV, downloadPDF } from "../api";

function ExportButtons() {
  return (
    <div className="card">
      <h2>6. Export Shortlist</h2>

      <button onClick={downloadCSV}>Download CSV</button>
      <button onClick={downloadPDF}>Download PDF</button>
    </div>
  );
}

export default ExportButtons;