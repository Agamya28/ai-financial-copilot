import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await api.get(
          "/analytics/summary"
        );

        setSummary(response.data);

      } catch (error) {
        console.error(error);
      }
    };

    loadData();
  }, []);

  if (!summary) {
    return <h2>Loading...</h2>;
  }

    return (
    <div>
        <h1>AI Financial Copilot</h1>

        <div>
        <h3>Total Spending</h3>
        <p>{summary.total_spending}</p>
        </div>

        <div>
        <h3>Transaction Count</h3>
        <p>{summary.transaction_count}</p>
        </div>

        <div>
        <h3>Average Transaction</h3>
        <p>{summary.average_transaction}</p>
        </div>

        <div>
        <h3>Largest Expense</h3>
        <p>{summary.largest_expense}</p>
        </div>
    </div>
    );
}

export default Dashboard;