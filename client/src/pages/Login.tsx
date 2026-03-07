import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="bg-slate-800 p-8 rounded-xl w-96 shadow-lg">
        <h2 className="text-2xl font-bold mb-6 text-center">
          SLA Breach Prevention
        </h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full mb-4 p-3 rounded bg-slate-700"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full mb-4 p-3 rounded bg-slate-700"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="w-full bg-indigo-600 hover:bg-indigo-700 p-3 rounded font-semibold">
          Login
        </button>
      </div>
    </div>
  );
}