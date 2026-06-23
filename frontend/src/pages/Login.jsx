import { useState } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";


function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const handleLogin = async () => {
    setError("");
  try {
    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    const response = await api.post(
      "/auth/login",
      formData,
      {
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
        },
      }
    );

    localStorage.setItem(
    "token",
    response.data.access_token
    );
    window.location.href = "/dashboard";
    } catch (error) {
        console.error(error);
         if (error.response?.status === 401) {
        setError("Invalid email or password.");
        } else {
            setError("Login failed. Please try again.");
        }
    }
    };
  return (
  <div className="min-h-screen bg-gray-100 flex items-center justify-center">
    <div className="bg-white p-8 rounded-xl shadow-md w-96">
      <h2 className="text-3xl font-bold mb-6 text-center">
        Login
      </h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full border border-gray-300 rounded-lg p-3 mb-4"
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full border border-gray-300 rounded-lg p-3 mb-6"
      />
        {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
        </div>
        )}
      <button
        onClick={handleLogin}
        className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700"
      >
        Login
      </button>
      <p className="mt-4 text-center">
  Don't have an account?

        <Link
            to="/register"
            className="text-blue-600 ml-2"
        >
            Sign Up
        </Link>
        </p>
    </div>
  </div>
);
}

export default Login;