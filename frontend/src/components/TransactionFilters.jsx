function TransactionFilters({
  filters,
  setFilters,
}) {

  const handleChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow mb-8">

      <h2 className="text-2xl font-semibold mb-4">
        Filter Transactions
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

        <select
          name="category"
          value={filters.category}
          onChange={handleChange}
          className="border p-3 rounded-lg"
        >
          <option value="">
            All Categories
          </option>

          <option value="food">
            Food
          </option>

          <option value="shopping">
            Shopping
          </option>

          <option value="transport">
            Transport
          </option>

          <option value="entertainment">
            Entertainment
          </option>

          <option value="health">
            Health
          </option>

        </select>

        <input
          type="text"
          name="merchant"
          placeholder="Search merchant"
          value={filters.merchant}
          onChange={handleChange}
          className="border p-3 rounded-lg"
        />

        <input
          type="date"
          name="startDate"
          value={filters.startDate}
          onChange={handleChange}
          className="border p-3 rounded-lg"
        />

        <input
          type="date"
          name="endDate"
          value={filters.endDate}
          onChange={handleChange}
          className="border p-3 rounded-lg"
        />

      </div>

    </div>
  );
}

export default TransactionFilters;