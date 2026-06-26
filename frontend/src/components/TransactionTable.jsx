function TransactionTable({ transactions, onDelete, onExport, title="Transactions", showDelete= true}) {
  return (
<div className="bg-white p-6 rounded-xl shadow mt-8">

  <div className="flex justify-between items-center mb-6">

    <h2 className="text-2xl font-semibold">
      {title}
    </h2>

    {!showDelete && (
      <button
        onClick={onExport}
        className="
          bg-green-600
          text-white
          px-4
          py-2
          rounded-lg
          hover:bg-green-700
        "
      >
        Export CSV
      </button>
    )}

  </div>

  <div className="overflow-x-auto">

    <table className="w-full">

      <thead>
        <tr className="border-b">
          <th className="text-left p-3">Date</th>
          <th className="text-left p-3">Category</th>
          <th className="text-left p-3">Merchant</th>
          <th className="text-left p-3">Amount</th>
          {showDelete && (
            <th className="text-left p-3">Actions</th>
          )}
        </tr>
      </thead>

      <tbody>
  {transactions.length === 0 ? (
    <tr>
      <td
        colSpan="4"
        className="p-4 text-center text-gray-500"
      >
        No transactions found
      </td>
    </tr>
  ) : (
    transactions.map((tx) => (
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

        {showDelete && (
          <td className="p-3">
            <button
              onClick={() => onDelete(tx.id)}
              className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
            >
              Delete
            </button>
          </td>
        )}
      </tr>
    ))
  )}
</tbody>

    </table>

  </div>

</div>
  );
}

export default TransactionTable;