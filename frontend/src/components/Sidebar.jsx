import { NavLink } from "react-router-dom";

export default function Sidebar() {
  const linkClass = ({ isActive }) =>
    `px-3 py-2 rounded ${
      isActive ? "bg-blue-500 text-white" : "hover:bg-gray-100"
    }`;

  return (
    <aside className="w-64 min-h-screen border-r p-4">
      <nav className="flex flex-col gap-2">

        <NavLink to="/" className={linkClass}>
          Dashboard
        </NavLink>

        <NavLink to="/transactions" className={linkClass}>
          Transactions
        </NavLink>

        <NavLink to="/budgets" className={linkClass}>
          Budgets
        </NavLink>

        <NavLink to="/reports" className={linkClass}>
          Reports
        </NavLink>

        <NavLink to="/profile" className={linkClass}>
          Profile
        </NavLink>

        <NavLink to="/settings" className={linkClass}>
          Settings
        </NavLink>

      </nav>
    </aside>
  );
}