import { useState } from "react";
import { startConversation, sendCandidateReply } from "../api";

function RealAgentChat({ candidate, onCandidateUpdate, onRankUpdate }) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  if (!candidate) return null;

  async function handleStartConversation() {
    setLoading(true);

    const data = await startConversation(candidate.id);

    onCandidateUpdate(data.candidate);

    setLoading(false);
  }

  async function handleSendReply() {
    if (!message.trim()) {
      alert("Please type candidate reply.");
      return;
    }

    setLoading(true);

    const data = await sendCandidateReply(candidate.id, message);

    onCandidateUpdate(data.candidate);

    if (onRankUpdate && data.ranked_candidates) {
      onRankUpdate(data.ranked_candidates);
    }

    setMessage("");
    setLoading(false);
  }

  return (
    <div>
      <h3>Real Agent Conversation</h3>

      <button onClick={handleStartConversation}>
        Start Agent Conversation
      </button>

      <div className="chat-box">
        {candidate.conversation && candidate.conversation.length > 0 ? (
          candidate.conversation.map((item, index) => (
            <div
              key={index}
              className={item.speaker === "Agent" ? "agent-message" : "candidate-message"}
            >
              <b>{item.speaker}:</b> {item.message}
            </div>
          ))
        ) : (
          <p>No conversation started yet.</p>
        )}
      </div>

      <textarea
        rows="3"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type candidate reply here..."
      />

      <button onClick={handleSendReply}>
        {loading ? "Agent thinking..." : "Send Candidate Reply"}
      </button>

      <div className="card-mini">
        <p><b>Interest Score:</b> {candidate.interest_score}</p>
        <p><b>Interest Level:</b> {candidate.interest_level || "Not assessed yet"}</p>
        <p><b>Interest Summary:</b> {candidate.interest_summary || "Not available"}</p>
      </div>
    </div>
  );
}

export default RealAgentChat;