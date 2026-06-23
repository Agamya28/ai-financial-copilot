import { useNavigate } from "react-router-dom";

export default function Navbar() {

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <header className="bg-white border-b px-6 py-4 flex justify-between items-center">

      <h1 className="text-2xl font-bold">
        AI Financial Copilot
      </h1>

      <button
        onClick={handleLogout}
        className="
          bg-red-500
          text-white
          px-4
          py-2
          rounded-lg
          hover:bg-red-600
          transition
        "
      >
        Logout
      </button>

    </header>
  );
}