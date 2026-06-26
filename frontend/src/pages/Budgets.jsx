import { useEffect, useState } from "react";
import api from "../services/api";
import BudgetForm from "../components/BudgetForm";
import BudgetTable from "../components/BudgetTable";

function Budgets() {
  const [budgets, setBudgets] = useState([]);

const handleDeleteBudget = async (category) => {

    const confirmed = window.confirm(
        `Are you sure you want to delete the ${category} budget?`
    );

    if (!confirmed) return;

    try {
        await api.delete(`/budget/${category}`);
        loadBudgets();
    } catch (error) {
        console.error(error);
    }
};

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
        <BudgetTable budgets={budgets} onDelete={handleDeleteBudget}/>
    </div>
    );
  
}
export default Budgets;