import { sendFeedback } from "../api";

function FeedbackButtons({ candidate, onFeedbackUpdate }) {
  async function handleFeedback(type) {
    await sendFeedback(
      candidate.id,
      type,
      `Recruiter marked ${candidate.name} as ${type}`
    );

    if (onFeedbackUpdate) {
      onFeedbackUpdate(type);
    }

    alert("Feedback saved: " + type);
  }

  return (
    <div>
      <h3>Recruiter Feedback</h3>

      <button onClick={() => handleFeedback("Shortlist")}>⭐ Shortlist</button>
      <button onClick={() => handleFeedback("Reject")}>❌ Reject</button>
      <button onClick={() => handleFeedback("Good Match")}>👍 Good Match</button>
      <button onClick={() => handleFeedback("Not Relevant")}>👎 Not Relevant</button>

      <p>
        <b>Current Feedback:</b> {candidate.recruiter_feedback || "Not reviewed"}
      </p>
    </div>
  );
}

export default FeedbackButtons;