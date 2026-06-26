import { useEffect, useState } from "react";
import api from "../services/api";
import TransactionTable from "../components/TransactionTable";
import TransactionForm from "../components/TransactionForm";
import CSVUpload from "../components/CSVUpload";
import TransactionFilters from "../components/TransactionFilters";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [filters, setFilters] = useState({
  category: "",
  merchant: "",
  startDate: "",
  endDate: "",
});
  const loadTransactions = async () => {
        try {
            const response =
                await api.get("/transactions/");

            setTransactions(response.data);
        } catch (error) {
            console.error(error);
        }
    };

        useEffect(() => {
            loadTransactions();
        }, []);


    const deleteTransaction = async (id) => {
        try {
            await api.delete(`/transactions/${id}`);
            loadTransactions();
        } catch (error) {
            console.error(error);
        }
    };
    const filteredTransactions =
  transactions.filter((tx) => {

    const matchesCategory =
        !filters.category ||
        tx.category.toLowerCase() ===
            filters.category.toLowerCase();

    const matchesMerchant =
      !filters.merchant ||
      tx.merchant
        .toLowerCase()
        .includes(
          filters.merchant.toLowerCase()
        );

    const matchesStartDate =
      !filters.startDate ||
      tx.transaction_date >= filters.startDate;

    const matchesEndDate =
      !filters.endDate ||
      tx.transaction_date <= filters.endDate;

    return (
      matchesCategory &&
      matchesMerchant &&
      matchesStartDate &&
      matchesEndDate
    );
  });

    return (
    <div className="p-8">
        <CSVUpload onUploadSuccess={loadTransactions}/>
        <TransactionForm onTransactionCreated={loadTransactions}/>
        <TransactionFilters filters={filters} setFilters={setFilters}/>
        <TransactionTable
        transactions={filteredTransactions}
        onDelete={deleteTransaction}
        title="All Transactions"
        />
    </div>
    );
}

export default Transactions;