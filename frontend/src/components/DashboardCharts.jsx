import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    PieChart,
    Pie,
    Cell,
  } from "recharts";
  
  const BAR_COLORS = {
    match: "#2563eb",
    interest: "#10b981",
    final: "#f59e0b",
  };
  
  const PIE_COLORS = ["#2563eb", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];
  
  function DashboardCharts({ candidates }) {
    if (!candidates || candidates.length === 0) return null;
  
    const chartData = candidates.map((candidate) => ({
      name: candidate.name,
      match: Number(candidate.match_score || 0),
      interest: Number(candidate.interest_score || 0),
      final: Number(candidate.final_score || 0),
    }));
  
    const totalCandidates = candidates.length;
  
    const avgMatch = (
      candidates.reduce((sum, c) => sum + Number(c.match_score || 0), 0) /
      totalCandidates
    ).toFixed(1);
  
    const avgInterest = (
      candidates.reduce((sum, c) => sum + Number(c.interest_score || 0), 0) /
      totalCandidates
    ).toFixed(1);
  
    const avgFinal = (
      candidates.reduce((sum, c) => sum + Number(c.final_score || 0), 0) /
      totalCandidates
    ).toFixed(1);
  
    const actionMap = {};
  
    candidates.forEach((candidate) => {
      const action = candidate.recommended_action || "Not Assigned";
      actionMap[action] = (actionMap[action] || 0) + 1;
    });
  
    const pieData = Object.keys(actionMap).map((key) => ({
      name: key,
      value: actionMap[key],
    }));
  
    return (
      <div className="card dashboard-wrapper">
        <h2>5. Dashboard Charts</h2>
  
        <div className="dashboard-metrics">
          <div className="metric-card metric-blue">
            <h3>{totalCandidates}</h3>
            <p>Total Candidates</p>
          </div>
  
          <div className="metric-card metric-green">
            <h3>{avgMatch}</h3>
            <p>Average Match Score</p>
          </div>
  
          <div className="metric-card metric-yellow">
            <h3>{avgInterest}</h3>
            <p>Average Interest Score</p>
          </div>
  
          <div className="metric-card metric-purple">
            <h3>{avgFinal}</h3>
            <p>Average Final Score</p>
          </div>
        </div>
  
        <div className="dashboard-chart-grid">
          <div className="chart-card">
            <h3>Candidate Score Comparison</h3>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={chartData} barCategoryGap="20%">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Legend />
                <Bar dataKey="match" fill={BAR_COLORS.match} radius={[6, 6, 0, 0]} name="Match Score" />
                <Bar dataKey="interest" fill={BAR_COLORS.interest} radius={[6, 6, 0, 0]} name="Interest Score" />
                <Bar dataKey="final" fill={BAR_COLORS.final} radius={[6, 6, 0, 0]} name="Final Score" />
              </BarChart>
            </ResponsiveContainer>
          </div>
  
          <div className="chart-card">
            <h3>Recommended Action Breakdown</h3>
            <ResponsiveContainer width="100%" height={350}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={110}
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={PIE_COLORS[index % PIE_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    );
  }
  
  export default DashboardCharts;