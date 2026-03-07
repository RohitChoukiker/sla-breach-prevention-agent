import { Link } from "react-router-dom";

export default function Sidebar({ role }: { role: string }) {
  return (
    <div className="w-64 bg-slate-800 h-screen p-6">
      <h1 className="text-xl font-bold mb-8">SLA Agent</h1>

      <ul className="space-y-4">
        <li>
          <Link to="/customer">Dashboard</Link>
        </li>

        {role === "customer" && (
          <li>
            <Link to="/customer/create">Create Ticket</Link>
          </li>
        )}
      </ul>
    </div>
  );
}