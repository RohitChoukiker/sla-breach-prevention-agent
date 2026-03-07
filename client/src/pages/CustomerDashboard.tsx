import { useState } from "react";
import type { Ticket } from "../types";
import { Link } from "react-router-dom";

//////////////////////////////////////////////////
// SAMPLE DATA (Demo Only)
//////////////////////////////////////////////////

const sampleTickets: Ticket[] = [
  {
    id: "1",
    title: "Production Server Down",
    description: "Main production API not responding.",
    urgency_requested: "critical",
    breach_probability: 0.92,
    confidence_score: 0.81,
    priority_final: "P1",
    status: "escalated",
  },
  {
    id: "2",
    title: "Payment Gateway Delay",
    description: "Users reporting slow checkout.",
    urgency_requested: "high",
    breach_probability: 0.67,
    confidence_score: 0.74,
    priority_final: "P2",
    status: "in_progress",
  },
  {
    id: "3",
    title: "UI Dropdown Bug",
    description: "Dropdown not selectable in dashboard.",
    urgency_requested: "medium",
    breach_probability: 0.38,
    confidence_score: 0.65,
    priority_final: "P3",
    status: "open",
  },
  {
    id: "4",
    title: "Password Reset Delay",
    description: "Reset email taking longer than expected.",
    urgency_requested: "low",
    breach_probability: 0.18,
    confidence_score: 0.59,
    priority_final: "P4",
    status: "open",
  },
];

//////////////////////////////////////////////////
// MAIN COMPONENT
//////////////////////////////////////////////////

export default function CustomerDashboard() {
  const [tickets] = useState<Ticket[]>(sampleTickets);

  const totalTickets = tickets.length;

  const highRisk = tickets.filter(
    (t) => t.breach_probability > 0.8
  ).length;

  const escalated = tickets.filter(
    (t) => t.status === "escalated"
  ).length;

  const avgRisk =
    tickets.length > 0
      ? (
          tickets.reduce(
            (sum, t) => sum + t.breach_probability,
            0
          ) / tickets.length
        ).toFixed(2)
      : "0";

  return (
    <div className="p-8 bg-slate-900 text-white min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center mb-10">
        <h1 className="text-3xl font-bold">
          SLA Risk Dashboard
        </h1>

        <Link
          to="/customer/create"
          className="bg-indigo-600 hover:bg-indigo-700 px-5 py-2 rounded-lg transition"
        >
          + Create Ticket
        </Link>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <SummaryCard title="Total Tickets" value={totalTickets} />
        <SummaryCard title="High Risk" value={highRisk} danger />
        <SummaryCard title="Escalated" value={escalated} danger />
        <SummaryCard
          title="Average Risk"
          value={`${(Number(avgRisk) * 100).toFixed(0)}%`}
        />
      </div>

      {/* Ticket Cards */}
      <div className="grid gap-6">
        {tickets.map((ticket) => (
          <TicketCard key={ticket.id} ticket={ticket} />
        ))}
      </div>
    </div>
  );
}

//////////////////////////////////////////////////
// Summary Card Component
//////////////////////////////////////////////////

function SummaryCard({
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
      className={`p-6 rounded-xl shadow-lg ${
        danger ? "bg-red-900/40 border border-red-600" : "bg-slate-800"
      }`}
    >
      <p className="text-slate-400">{title}</p>
      <h2 className="text-2xl font-bold mt-2">{value}</h2>
    </div>
  );
}

//////////////////////////////////////////////////
// Ticket Card Component
//////////////////////////////////////////////////

function TicketCard({ ticket }: { ticket: Ticket }) {
  let riskColor = "bg-green-500";

  if (ticket.breach_probability > 0.8)
    riskColor = "bg-red-500";
  else if (ticket.breach_probability > 0.6)
    riskColor = "bg-orange-500";
  else if (ticket.breach_probability > 0.4)
    riskColor = "bg-yellow-500";

  return (
    <div className="bg-slate-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-lg font-semibold">
          {ticket.title}
        </h3>

        {ticket.status === "escalated" && (
          <span className="text-red-400 font-semibold">
            🚨 Escalated
          </span>
        )}
      </div>

      <p className="text-slate-400 mb-5">
        {ticket.description}
      </p>

      <div className="flex justify-between items-center mb-2">
        <span className="text-sm text-slate-400">
          Breach Probability
        </span>

        <span
          className={`${riskColor} px-3 py-1 rounded text-sm font-semibold`}
        >
          {(ticket.breach_probability * 100).toFixed(0)}%
        </span>
      </div>

      <div className="flex justify-between text-sm text-slate-400">
        <span>
          Confidence: {(ticket.confidence_score * 100).toFixed(0)}%
        </span>
        <span>Priority: {ticket.priority_final}</span>
      </div>
    </div>
  );
}