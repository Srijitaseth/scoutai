function AgentConversation({ conversation }) {
    if (!conversation || conversation.length === 0) {
      return null;
    }
  
    return (
      <div>
        <h3>Simulated Agent Conversation</h3>
  
        <div className="chat-box">
          {conversation.map((item, index) => (
            <div
              key={index}
              className={item.speaker === "Agent" ? "agent-message" : "candidate-message"}
            >
              <b>{item.speaker}:</b> {item.message}
            </div>
          ))}
        </div>
      </div>
    );
  }
  
  export default AgentConversation;