import { useEffect, useState } from "react";
import api from "../services/api";
import BudgetForm from "../components/BudgetForm";
import BudgetTable from "../components/BudgetTable";

function Budgets() {
  const [budgets, setBudgets] = useState([]);

  const loadBudgets = async () => {
        try {
            const response =
                await api.get("/budget/status");

            setBudgets(response.data);
        } catch (error) {
            console.error(error);
        }
    };

        useEffect(() => {
            loadBudgets();
        }, []);

    return (
    <div className="p-8">
        <BudgetForm onBudgetAdded={loadBudgets} />
        <BudgetTable budgets={budgets} />
    </div>
    );
  
}
export default Budgets;