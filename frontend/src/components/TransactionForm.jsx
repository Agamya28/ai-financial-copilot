import { useState } from "react";
import api from "../services/api";

function TransactionForm({onTransactionCreated}) {
    const [formData, setFormData] = useState({
        amount: "",
        category: "",
        merchant: "",
        description: "",
        transaction_date: "",
    });
    const [success, setSuccess] = useState("");

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
            "/transactions/",
            formData
        );

        setSuccess(
            "Transaction added successfully!"
        );

        if (onTransactionCreated) {
            await onTransactionCreated();
        }

        setFormData({
            amount: "",
            category: "",
            merchant: "",
            description: "",
            transaction_date: "",
        });

    } catch (error) {

        console.error(error);
        console.log(error.response?.data);
        setSuccess(
            "Failed to add transaction."
        );
    }
};

    return (
        <div className="bg-white p-6 rounded-xl shadow mb-8">
            <h2 className="text-2xl font-semibold mb-6">
                Add Transaction
            </h2>
            {success && (
                <div className="mb-4 p-3 rounded bg-green-100">
                    {success}
                </div>
            )}
            <form
                onSubmit={handleSubmit}
                className="grid grid-cols-1 md:grid-cols-2 gap-4"
            >
                <div>
                    <label
                        htmlFor="amount"
                        className="block mb-1 font-medium"
                    >
                        Amount
                    </label>

                    <input
                        type="number"
                        name="amount"
                        value={formData.amount}
                        onChange={handleChange}
                        min="0"
                        className="w-full border rounded-lg p-2"
                    />
                </div>

                <div>
                    <label
                        htmlFor="category"
                        className="block mb-1 font-medium"
                    >
                        Category
                    </label>

                    <input
                        type="text"
                        name="category"
                        value={formData.category}
                        onChange={handleChange}
                        className="w-full border rounded-lg p-2"
                    />
                </div>

                <div>
                    <label
                        htmlFor="merchant"
                        className="block mb-1 font-medium"
                    >
                        Merchant
                    </label>

                    <input
                        type="text"
                        name="merchant"
                        value={formData.merchant}
                        onChange={handleChange}
                        className="w-full border rounded-lg p-2"
                    />
                </div>

                <div>
                    <label
                        htmlFor="transaction_date"
                        className="block mb-1 font-medium"
                    >
                        Transaction Date
                    </label>

                    <input
                        type="date"
                        name="transaction_date"
                        value={formData.transaction_date}
                        onChange={handleChange}
                        className="w-full border rounded-lg p-2"
                    />
                </div>

                <div className="md:col-span-2">
                    <label
                        htmlFor="description"
                        className="block mb-1 font-medium"
                    >
                        Description
                    </label>

                    <input
                        type="text"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        className="w-full border rounded-lg p-2"
                    />
                </div>

                <div className="md:col-span-2">
                    <button
                        type="submit"
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
                    >
                        Add Transaction
                    </button>
                </div>
            </form>
        </div>
    );
}

export default TransactionForm;