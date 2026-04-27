import FeedbackButtons from "./FeedbackButtons";
import SendEmailButton from "./SendEmailButton";

function CandidateDetails({
  candidate,
  onFeedbackUpdate,
}) {
  if (!candidate) return null;

  const parsedResume = candidate.parsed_resume || {};

  return (
    <div className="card">
      <h2>4. Candidate Details</h2>

      <p><b>Name:</b> {candidate.name}</p>
      <p><b>Email:</b> {candidate.email}</p>
      <p><b>Phone:</b> {candidate.phone || "Not found"}</p>
      <p><b>Match Score:</b> {candidate.match_score}</p>
      <p><b>Interest Score:</b> {candidate.interest_score}</p>
      <p><b>Final Score:</b> {candidate.final_score}</p>
      <p><b>Recruiter Feedback:</b> {candidate.recruiter_feedback || "Not reviewed"}</p>

      <h3>Parsed Resume Summary</h3>
      <p>{parsedResume.summary || "No summary found"}</p>

      <h3>Education</h3>
      <pre>{JSON.stringify(parsedResume.education || [], null, 2)}</pre>

      <h3>Experience</h3>
      <pre>{JSON.stringify(parsedResume.experience || [], null, 2)}</pre>

      <h3>Projects</h3>
      <pre>{JSON.stringify(parsedResume.projects || [], null, 2)}</pre>

      <h3>Matched Skills</h3>
      <p>{candidate.matched_skills?.join(", ") || "None"}</p>

      <h3>Missing Skills</h3>
      <p>{candidate.missing_skills?.join(", ") || "None"}</p>

      <h3>Why Matched</h3>
      <ul>
        {candidate.explanation?.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>

      <h3>Generated Outreach Email</h3>
      <pre>{candidate.outreach_email}</pre>

      <SendEmailButton candidate={candidate} />

      <FeedbackButtons
        candidate={candidate}
        onFeedbackUpdate={onFeedbackUpdate}
      />
    </div>
  );
}

export default CandidateDetails;