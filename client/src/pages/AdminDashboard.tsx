import { useState } from "react";

/////////////////////////////////////////////////////////
// SAMPLE DATA
/////////////////////////////////////////////////////////

type Role = "customer" | "agent" | "admin";

interface User {
  id: string;
  name: string;
  role: Role;
}

interface Ticket {
  id: string;
  title: string;
  breach_probability: number;
  confidence_score: number;
  status: string;
  assigned_agent?: string;
}

const sampleUsers: User[] = [
  { id: "1", name: "Rohit", role: "admin" },
  { id: "2", name: "Amit", role: "agent" },
  { id: "3", name: "Neha", role: "customer" },
];

const sampleTickets: Ticket[] = [
  {
    id: "T1",
    title: "Production Server Down",
    breach_probability: 0.91,
    confidence_score: 0.83,
    status: "escalated",
  },
  {
    id: "T2",
    title: "Payment API Delay",
    breach_probability: 0.72,
    confidence_score: 0.75,
    status: "in_progress",
  },
];

/////////////////////////////////////////////////////////
// MAIN ADMIN DASHBOARD
/////////////////////////////////////////////////////////

export default function AdminDashboard() {
  const [users, setUsers] = useState(sampleUsers);
  const [tickets, setTickets] = useState(sampleTickets);
  const [threshold, setThreshold] = useState(0.8);

  const escalatedTickets = tickets.filter(
    (t) => t.status === "escalated"
  );

  const avgRisk =
    tickets.length > 0
      ? (
          tickets.reduce(
            (sum, t) => sum + t.breach_probability,
            0
          ) / tickets.length
        ).toFixed(2)
      : "0";

  /////////////////////////////////////////////////////////
  // HANDLERS
  /////////////////////////////////////////////////////////

  const changeUserRole = (id: string, role: Role) => {
    const updated = users.map((u) =>
      u.id === id ? { ...u, role } : u
    );
    setUsers(updated);
  };

  const assignAgent = (ticketId: string, agentName: string) => {
    const updated = tickets.map((t) =>
      t.id === ticketId
        ? { ...t, assigned_agent: agentName }
        : t
    );
    setTickets(updated);
  };

  const overrideAI = (ticketId: string) => {
    alert(`AI decision overridden for ${ticketId}`);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-10">
        Admin Control Panel
      </h1>

      {/* ================= OVERVIEW ================= */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <Card title="Total Tickets" value={tickets.length} />
        <Card
          title="Escalated"
          value={escalatedTickets.length}
          danger
        />
        <Card
          title="Average Risk"
          value={`${(Number(avgRisk) * 100).toFixed(0)}%`}
        />
      </section>

      {/* ================= ESCALATION QUEUE ================= */}
      <section className="bg-white p-6 rounded-xl shadow mb-12">
        <h2 className="text-xl font-semibold mb-6">
          Escalation Queue
        </h2>

        {escalatedTickets.map((ticket) => (
          <div
            key={ticket.id}
            className="flex justify-between items-center border-b py-4"
          >
            <div>
              <h3 className="font-semibold">
                {ticket.title}
              </h3>
              <p className="text-sm text-gray-500">
                Prob: {(ticket.breach_probability * 100).toFixed(0)}% | Conf:{" "}
                {(ticket.confidence_score * 100).toFixed(0)}%
              </p>
            </div>

            <div className="flex gap-3">
              <select
                onChange={(e) =>
                  assignAgent(ticket.id, e.target.value)
                }
                className="border px-3 py-2 rounded"
              >
                <option>Select Agent</option>
                {users
                  .filter((u) => u.role === "agent")
                  .map((agent) => (
                    <option key={agent.id}>
                      {agent.name}
                    </option>
                  ))}
              </select>

              <button
                onClick={() => overrideAI(ticket.id)}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Override AI
              </button>
            </div>
          </div>
        ))}
      </section>

      {/* ================= USER MANAGEMENT ================= */}
      <section className="bg-white p-6 rounded-xl shadow mb-12">
        <h2 className="text-xl font-semibold mb-6">
          User Management
        </h2>

        {users.map((user) => (
          <div
            key={user.id}
            className="flex justify-between items-center border-b py-4"
          >
            <span>{user.name}</span>

            <select
              value={user.role}
              onChange={(e) =>
                changeUserRole(user.id, e.target.value as Role)
              }
              className="border px-3 py-2 rounded"
            >
              <option value="customer">Customer</option>
              <option value="agent">Agent</option>
              <option value="admin">Admin</option>
            </select>
          </div>
        ))}
      </section>

      {/* ================= THRESHOLD CONFIG ================= */}
      <section className="bg-white p-6 rounded-xl shadow mb-12">
        <h2 className="text-xl font-semibold mb-6">
          Threshold Configuration
        </h2>

        <div className="flex items-center gap-4">
          <span>Escalation Threshold:</span>
          <input
            type="number"
            step="0.1"
            min="0"
            max="1"
            value={threshold}
            onChange={(e) =>
              setThreshold(Number(e.target.value))
            }
            className="border px-3 py-2 rounded w-24"
          />
        </div>
      </section>

      {/* ================= ANALYTICS ================= */}
      <section className="bg-white p-6 rounded-xl shadow mb-12">
        <h2 className="text-xl font-semibold mb-6">
          Analytics Overview
        </h2>

        <ul className="space-y-2 text-gray-600">
          <li>High Risk Tickets: {tickets.filter(t => t.breach_probability > 0.8).length}</li>
          <li>Breached Tickets: 1 (Demo)</li>
          <li>Resolved Today: 3 (Demo)</li>
        </ul>
      </section>

      {/* ================= AUDIT LOGS ================= */}
      <section className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-xl font-semibold mb-6">
          Audit Logs
        </h2>

        <ul className="space-y-2 text-sm text-gray-600">
          <li>AI escalated Ticket T1</li>
          <li>Admin assigned agent to Ticket T1</li>
          <li>User role changed for Amit</li>
        </ul>
      </section>
    </div>
  );
}

/////////////////////////////////////////////////////////
// CARD COMPONENT
/////////////////////////////////////////////////////////

function Card({
  title,
  value,
  danger = false,
}: {
  title: string;
  value: any;
  danger?: boolean;
}) {
  return (
    <div
      className={`p-6 rounded-xl shadow ${
        danger
          ? "bg-red-100 border border-red-400"
          : "bg-white"
      }`}
    >
      <p className="text-gray-500">{title}</p>
      <h2 className="text-2xl font-bold mt-2 text-gray-800">
        {value}
      </h2>
    </div>
  );
}