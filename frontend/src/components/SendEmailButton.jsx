import { sendOutreachEmail } from "../api";

function SendEmailButton({ candidate }) {
  async function handleSendEmail() {
    if (!candidate.email || candidate.email === "not_found@email.com") {
      alert("Candidate email not found.");
      return;
    }

    const emailText = candidate.outreach_email || "";

    const lines = emailText.split("\n");

    let subject = "Opportunity from ScoutAI";
    let body = emailText;

    if (lines[0].startsWith("Subject:")) {
      subject = lines[0].replace("Subject:", "").trim();
      body = lines.slice(1).join("\n").trim();
    }

    const result = await sendOutreachEmail(candidate.email, subject, body);

    if (result.success) {
      alert(result.message);
    } else {
      alert("Email failed: " + result.message);
    }
  }

  return (
    <button onClick={handleSendEmail}>
      Send Email
    </button>
  );
}

export default SendEmailButton;