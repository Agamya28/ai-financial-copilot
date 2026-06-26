import { useState } from "react";
import api from "../services/api";

function BudgetForm({ onBudgetAdded }) {
  const [formData, setFormData] = useState({
    category: "",
    monthly_limit: "",
  });

  const categories = [
    "food",
    "shopping",
    "transport",
    "entertainment",
    "health",
  ];
  const handleChange = (e) => {  
    setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    const handleSubmit = async (e) => {
    e.preventDefault();

        try {

            await api.post(
                "/budget/",
                formData
            );

            setFormData({
                category: "",
                monthly_limit: "",
            });

            onBudgetAdded();

        } catch (error) {
            alert(
            error.response?.data?.detail ||
            "Failed to create budget."
        );
        }
    };

    return (
  <div className="bg-white p-6 rounded-xl shadow mb-8">

    <h2 className="text-2xl font-semibold mb-6">
      Add Budget
    </h2>

    <form
      onSubmit={handleSubmit}
      className="grid grid-cols-1 md:grid-cols-2 gap-4">

      {/* Category dropdown */}
        <select
  name="category"
  value={formData.category}
  onChange={handleChange}
  className="border p-3 rounded-lg"
  required
>
  <option value="">
    Select Category
  </option>

  {categories.map((category) => (
    <option
      key={category}
      value={category}
    >
      {category}
    </option>
  ))}
</select>
      {/* Monthly limit input */}
        <input
            type="number"
            name="monthly_limit"
            placeholder="Monthly Limit"
            value={formData.monthly_limit}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            min="0"
            required
            />
      {/* Submit button */}
        <button type="submit" className="bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 md:col-span-2">
            Add Budget
        </button>
    </form>

  </div>
);
}

export default BudgetForm;