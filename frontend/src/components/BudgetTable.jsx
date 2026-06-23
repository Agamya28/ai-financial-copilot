function BudgetTable({ budgets }) {
    return (
        <div className="bg-white p-6 rounded-xl shadow mt-8">

            <h2 className="text-2xl font-semibold mb-4">
                Budget Overview
            </h2>

            <div className="overflow-x-auto">

                <table className="w-full">

                    <thead>
                        <tr className="border-b">

                            <th className="text-left p-3">
                                Category
                            </th>

                            <th className="text-left p-3">
                                Limit
                            </th>

                            <th className="text-left p-3">
                                Spent
                            </th>

                            <th className="text-left p-3">
                                Remaining
                            </th>

                            <th className="text-left p-3">
                                Used %
                            </th>

                            <th className="text-left p-3">
                                Status
                            </th>

                        </tr>
                    </thead>

                    <tbody>

                        {budgets.map((budget) => (

                            <tr
                                key={budget.category}
                                className="border-b hover:bg-gray-50"
                            >

                                <td className="p-3 capitalize">
                                    {budget.category}
                                </td>

                                <td className="p-3">
                                    ₹{Number(
                                        budget.monthly_limit
                                    ).toFixed(2)}
                                </td>

                                <td className="p-3">
                                    ₹{Number(
                                        budget.spent
                                    ).toFixed(2)}
                                </td>

                                <td className="p-3">
                                    ₹{Number(
                                        budget.remaining
                                    ).toFixed(2)}
                                </td>

                                <td className="p-3">
                                    {budget.percentage_used}%
                                </td>

                                <td
                                    className={`p-3 font-semibold ${
                                        budget.percentage_used > 100
                                            ? "text-red-600"
                                            : "text-green-600"
                                    }`}
                                >
                                    {budget.percentage_used > 100
                                        ? "Over Budget"
                                        : "Within Budget"}
                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>
    );
}

export default BudgetTable;