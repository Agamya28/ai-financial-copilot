import { useEffect, useState } from "react";
import api from "../services/api";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Legend,
} from "recharts";

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [monthlyData, setMonthlyData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [advancedData, setAdvancedData] = useState(null);
  const [insights, setInsights] = useState([]);
  const [budgetStatus, setBudgetStatus] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  const formatMonth = (monthString) => {
  const date = new Date(`${monthString}-01`);

    return date.toLocaleString("en-US", {
        month: "long",
        year: "numeric",
    });
    };
    const getProgressColor = (percentage) => {
    if (percentage >= 90) {
        return "bg-red-500";
    }

    if (percentage >= 70) {
        return "bg-yellow-500";
    }

    return "bg-green-500";
    };
  useEffect(() => {
    const loadData = async () => {
        
      try {
        
        const summaryResponse = await api.get(
          "/analytics/summary"
        );

        setSummary(summaryResponse.data);

        const monthlyResponse = await api.get(
          "/analytics/monthly-spending"
        );

        setMonthlyData(monthlyResponse.data);

        const categoryResponse = await api.get(
          "/analytics/category_breakdown"
        );

        setCategoryData(
          categoryResponse.data.map((item) => ({
            ...item,
            total_spending: Number(
              item.total_spending
            ),
          }))
        );
        const advancedResponse = await api.get(
        "/analytics/advanced"
        );

        setAdvancedData(
        advancedResponse.data
        );

        const insightsResponse = await api.get(
        "/analytics/insights"
        );

        setInsights(insightsResponse.data);
        const budgetResponse = await api.get(
        "/budget/status"
        );

        setBudgetStatus(budgetResponse.data);

        const transactionResponse =
        await api.get("/transactions/");

        setTransactions(transactionResponse.data);
        const recommendationResponse =
        await api.get(
            "/analytics/budget-recommendations"
        );

        setRecommendations(
        recommendationResponse.data
        );

      } catch (error) {
        console.error(error);

        console.log(
          "Response data:"
        );

        console.log(
          error.response?.data
        );
      }
    };

    loadData();
  }, []);

  if (!summary) {
    return (
      <h2 className="p-8 text-xl">
        Loading...
      </h2>
    );
  }
  
  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <h1 className="text-4xl font-bold mb-8">
        AI Financial Copilot
      </h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-gray-500">
            Total Spending
          </h3>

          <p className="text-2xl font-bold">
            ₹{Number(summary.total_spending).toFixed(2)}
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-gray-500">
            Transactions
          </h3>

          <p className="text-2xl font-bold">
            {summary.transaction_count}
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-gray-500">
            Average Transaction
          </h3>

          <p className="text-2xl font-bold">
            ₹{Number(summary.average_transaction).toFixed(2)}
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-gray-500">
            Largest Expense
          </h3>

          <p className="text-2xl font-bold">
            ₹{Number(summary.largest_expense).toFixed(2)}
          </p>
        </div>

      </div>
        {/* Budget Status */}

        <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">
            Budget Tracking
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

            {budgetStatus.map((budget) => (
            <div
                key={budget.category}
                className="bg-white p-6 rounded-xl shadow"
            >
                <div className="flex justify-between mb-2">
                <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold capitalize">
                    {budget.category}
                </h3>

                {budget.percentage_used > 100 && (
                    <span className="text-red-600 font-bold ml-3">
                    Over Budget
                    </span>
                )}
                </div>


                <span className="text-sm text-gray-500">
                    {budget.percentage_used}%
                </span>
                </div>

                <div className="w-full bg-gray-200 rounded-full h-3 mb-4">

                <div
                    className={`h-3 rounded-full ${getProgressColor(
                    budget.percentage_used
                    )}`}
                    style={{
                    width: `${Math.min(
                        budget.percentage_used,
                        100
                    )}%`,
                    }}
                />

                </div>

                <p>
                Spent:
                <span className="font-semibold">
                    {" "}
                    ₹{Number(budget.spent).toFixed(2)}
                </span>
                </p>

                <p>
                Remaining:
                <span className="font-semibold">
                    {" "}
                    ₹{Number(
                    budget.remaining
                    ).toFixed(2)}
                </span>
                </p>

                <p>
                Limit:
                <span className="font-semibold">
                    {" "}
                    ₹{Number(
                    budget.monthly_limit
                    ).toFixed(2)}
                </span>
                </p>
            </div>
            ))}

        </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow mb-8">

        <h2 className="text-2xl font-semibold mb-4">
            Budget Recommendations
        </h2>

        {recommendations.map((rec, index) => (

            <div
            key={index}
            className={`border-l-4 pl-4 py-2 mb-3 bg-gray-50 ${
                rec.message.includes("exceed")
                ? "border-red-500"
                : "border-green-500"
            }`}
            >

            <p className="font-semibold capitalize">
                {rec.category}
            </p>

            <p>
                {rec.message}
            </p>

            </div>

        ))}

        </div>
      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* Monthly Spending */}
        <div className="bg-white p-6 rounded-xl shadow">

          <h2 className="text-xl font-semibold mb-4">
            Monthly Spending
          </h2>

          <ResponsiveContainer
            width="100%"
            height={300}
          >
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />

              <XAxis
                dataKey="month"
                tickFormatter={(value) =>
                    new Date(`${value}-01`).toLocaleString(
                    "en-US",
                    {
                        month: "short",
                        year: "2-digit",
                    }
                    )
                }
                />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="total_spending"
              />
            </LineChart>
          </ResponsiveContainer>

        </div>

        {/* Category Distribution */}
        <div className="bg-white p-6 rounded-xl shadow">

          <h2 className="text-xl font-semibold mb-4">
            Category Distribution
          </h2>

          <ResponsiveContainer
            width="100%"
            height={350}
          >
            <PieChart>

              <Pie
                data={categoryData}
                dataKey="total_spending"
                nameKey="category"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              />

              <Tooltip />

              <Legend />

            </PieChart>
          </ResponsiveContainer>

        </div>

      </div>
              <div className="bg-white p-6 rounded-xl shadow mt-8">
        <h2 className="text-2xl font-semibold mb-4">
            AI Insights
        </h2>

        {insights.map((insight, index) => (
            <div
            key={index}
            className="border-l-4 border-blue-500 pl-4 py-2 mb-3 bg-gray-50"
            >
            {insight}
            </div>
        ))}
        </div>
      {advancedData && (
        <div className="mt-8 bg-white p-6 rounded-xl shadow">

            <h2 className="text-2xl font-semibold mb-6">
            Spending Insights
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

            <div>
                <h3 className="font-semibold">
                Top Category
                </h3>

                <p>
                {advancedData.top_category?.category}
                </p>

                <p>
                ₹{
                    Number(
                    advancedData.top_category?.total_spending
                    ).toFixed(2)
                }
                </p>
            </div>

            <div>
                <h3 className="font-semibold">
                Highest Spending Month
                </h3>

                <p>
                {formatMonth(
                    advancedData.highest_spending_month?.month
                )}
                </p>

                <p>
                ₹{
                    Number(
                    advancedData.highest_spending_month?.total_spending
                    ).toFixed(2)
                }
                </p>
            </div>

            <div>
                <h3 className="font-semibold">
                Lowest Spending Month
                </h3>

                <p>
                {formatMonth(
                    advancedData.lowest_spending_month?.month
                )}
                </p>

                <p>
                ₹{
                    Number(
                    advancedData.lowest_spending_month?.total_spending
                    ).toFixed(2)
                }
                </p>
            </div>

            </div>

        </div>
        )}

        {advancedData && (
  <div className="mt-8 bg-white p-6 rounded-xl shadow">
    ...
  </div>
)}

{/* Recent Transactions */}
<div className="bg-white p-6 rounded-xl shadow mt-8">

  <h2 className="text-2xl font-semibold mb-4">
    Recent Transactions
  </h2>

  <div className="overflow-x-auto">

    <table className="w-full">

      <thead>
        <tr className="border-b">
          <th className="text-left p-3">Date</th>
          <th className="text-left p-3">Category</th>
          <th className="text-left p-3">Merchant</th>
          <th className="text-left p-3">Amount</th>
        </tr>
      </thead>

      <tbody>

        {transactions.map((tx) => (
          <tr
            key={tx.id}
            className="border-b hover:bg-gray-50"
          >
            <td className="p-3">
              {tx.transaction_date}
            </td>

            <td className="p-3 capitalize">
              {tx.category}
            </td>

            <td className="p-3">
              {tx.merchant}
            </td>

            <td className="p-3 font-semibold">
              ₹{Number(tx.amount).toFixed(2)}
            </td>
          </tr>
        ))}

      </tbody>

    </table>

  </div>

</div>

</div>
);


}

export default Dashboard;