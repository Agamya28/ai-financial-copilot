import { useState } from "react";
import api from "../services/api";
import ReactMarkdown from "react-markdown";
import jsPDF from "jspdf";

function Reports() {

    const [report, setReport] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const generateReport = async () => {

        try {

            setLoading(true);
            setError("");

            const response = await api.get("/ai/report");

            setReport(response.data.report);

        } catch (error) {

            setError(
                error.response?.data?.detail ||
                "Failed to generate report."
            );

        } finally {
            setLoading(false);
        }
    };

    const downloadPDF = () => {
        const doc = new jsPDF();

        const cleanReport = report
        .replace(/₹/g, "Rs.")
        .replace(/[^\x00-\x7F]/g, "");

        const lines = doc.splitTextToSize(
            cleanReport,
            180
        );

        doc.text(lines, 10, 10);

        doc.save("financial-report.pdf");
    };

    const downloadCSV = () => {

    const rows = report
        .split("\n")
        .filter(line => line.trim() !== "");

    const csvContent = [
        ["Financial Report"],
        ...rows.map(line => [line])
    ]
    .map(row =>
        row.map(field =>
            `"${field.replace(/"/g, '""')}"`
        ).join(",")
    )
    .join("\n");

    const blob = new Blob(
        [csvContent],
        { type: "text/csv;charset=utf-8;" }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "financial-report.csv";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);
};

    return (
        <div className="p-8">

            <div className="bg-white rounded-xl shadow p-6">

                <h1 className="text-3xl font-bold mb-4">
                    AI Financial Health Report
                </h1>

                <p className="text-gray-600 mb-6">
                    Generate a personalized AI-powered financial report
                    based on your spending patterns, budgets, and analytics.
                </p>

                <button
                    onClick={generateReport}
                    disabled={loading}
                    className="
                        bg-blue-600
                        text-white
                        px-6
                        py-3
                        rounded-lg
                        hover:bg-blue-700
                        disabled:bg-gray-400
                    "
                >
                    {loading
                        ? "Generating..."
                        : "Generate Report"}
                </button>

                {error && (
                    <p className="text-red-500 mt-4">
                        {error}
                    </p>
                )}

                {report && (
    <div className="mt-8">

        <div className="flex gap-4 mb-4">

            <button
                onClick={downloadPDF}
                className="
                    bg-green-600
                    text-white
                    px-4
                    py-2
                    rounded
                    hover:bg-green-700
                "
            >
                Download PDF
            </button>

            <button
                onClick={downloadCSV}
                className="
                    bg-blue-600
                    text-white
                    px-4
                    py-2
                    rounded
                    hover:bg-blue-700
                "
            >
                Export CSV
            </button>

        </div>

        <h2 className="text-2xl font-semibold mb-4">
            Your Financial Report
        </h2>

        <div
            className="
                bg-gray-50
                p-6
                rounded-lg
                whitespace-pre-wrap
                leading-8
                prose
                max-w-none
            "
        >
            <ReactMarkdown>
                {report}
            </ReactMarkdown>
        </div>

    </div>
)}
                
            </div>

        </div>
    );
}

export default Reports;