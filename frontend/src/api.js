const BASE_URL = (import.meta.env.VITE_BACKEND_URL || "/api").replace(/\/$/, "");

export async function analyzeResumes(jdText, files) {
  const formData = new FormData();
  formData.append("jd_text", jdText);

  for (let file of files) {
    formData.append("files", file);
  }

  const response = await fetch(`${BASE_URL}/upload-resumes`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}

export async function startConversation(candidateId) {
  const formData = new FormData();
  formData.append("candidate_id", candidateId);

  const response = await fetch(`${BASE_URL}/start-conversation`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}

export async function sendCandidateReply(candidateId, message) {
  const formData = new FormData();
  formData.append("candidate_id", candidateId);
  formData.append("message", message);

  const response = await fetch(`${BASE_URL}/candidate-reply`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}

export async function sendFeedback(candidateId, feedbackType, comment) {
  const formData = new FormData();
  formData.append("candidate_id", candidateId);
  formData.append("feedback_type", feedbackType);
  formData.append("comment", comment);

  const response = await fetch(`${BASE_URL}/feedback`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}

export async function sendOutreachEmail(toEmail, subject, body) {
  const formData = new FormData();
  formData.append("to_email", toEmail);
  formData.append("subject", subject);
  formData.append("body", body);

  const response = await fetch(`${BASE_URL}/send-email`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}

export function downloadCSV() {
  window.open(`${BASE_URL}/export/csv`, "_blank");
}

export function downloadPDF() {
  window.open(`${BASE_URL}/export/pdf`, "_blank");
}
