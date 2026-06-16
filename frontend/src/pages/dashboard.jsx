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

  const formatMonth = (monthString) => {
  const date = new Date(`${monthString}-01`);

    return date.toLocaleString("en-US", {
        month: "long",
        year: "numeric",
    });
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



    </div>
  );
}

export default Dashboard;