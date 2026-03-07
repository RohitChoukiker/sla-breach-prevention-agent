import { useState } from "react";
import type { Ticket } from "../types";

//////////////////////////////////////////////////
// SAMPLE DATA (Agent Assigned Tickets)
//////////////////////////////////////////////////

const sampleAssignedTickets: Ticket[] = [
  {
    id: "1",
    title: "Production Server Down",
    description: "API completely unavailable.",
    urgency_requested: "critical",
    breach_probability: 0.91,
    confidence_score: 0.83,
    priority_final: "P1",
    status: "escalated",
  },
  {
    id: "2",
    title: "Payment Gateway Delay",
    description: "Checkout latency high.",
    urgency_requested: "high",
    breach_probability: 0.72,
    confidence_score: 0.75,
    priority_final: "P2",
    status: "in_progress",
  },
  {
    id: "3",
    title: "Minor UI Bug",
    description: "Dropdown misaligned.",
    urgency_requested: "low",
    breach_probability: 0.22,
    confidence_score: 0.61,
    priority_final: "P4",
    status: "open",
  },
];

//////////////////////////////////////////////////
// MAIN COMPONENT
//////////////////////////////////////////////////

export default function AgentDashboard() {
  const [tickets, setTickets] = useState<Ticket[]>(
    [...sampleAssignedTickets].sort(
      (a, b) => b.breach_probability - a.breach_probability
    )
  );

  const updateStatus = (id: string, newStatus: string) => {
    const updated = tickets.map((ticket) =>
      ticket.id === id
        ? { ...ticket, status: newStatus }
        : ticket
    );
    setTickets(updated);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        Agent Work Queue
      </h1>

      <div className="grid gap-6">
        {tickets.map((ticket) => (
          <AgentTicketCard
            key={ticket.id}
            ticket={ticket}
            onUpdate={updateStatus}
          />
        ))}
      </div>
    </div>
  );
}

//////////////////////////////////////////////////
// Ticket Card for Agent
//////////////////////////////////////////////////

function AgentTicketCard({
  ticket,
  onUpdate,
}: {
  ticket: Ticket;
  onUpdate: (id: string, status: string) => void;
}) {
  let riskColor = "bg-green-500";

  if (ticket.breach_probability > 0.8)
    riskColor = "bg-red-500";
  else if (ticket.breach_probability > 0.6)
    riskColor = "bg-orange-500";
  else if (ticket.breach_probability > 0.4)
    riskColor = "bg-yellow-500";

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold text-gray-800">
          {ticket.title}
        </h2>

        {ticket.status === "escalated" && (
          <span className="text-red-600 font-semibold">
            🚨 Escalated
          </span>
        )}
      </div>

      <p className="text-gray-600 mb-4">
        {ticket.description}
      </p>

      {/* Risk Info */}
      <div className="flex justify-between items-center mb-3">
        <span className="text-sm text-gray-500">
          Breach Probability
        </span>

        <span
          className={`${riskColor} text-white px-3 py-1 rounded text-sm font-semibold`}
        >
          {(ticket.breach_probability * 100).toFixed(0)}%
        </span>
      </div>

      <div className="flex justify-between text-sm text-gray-500 mb-4">
        <span>
          Confidence: {(ticket.confidence_score * 100).toFixed(0)}%
        </span>
        <span>Priority: {ticket.priority_final}</span>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        {ticket.status !== "in_progress" && (
          <button
            onClick={() => onUpdate(ticket.id, "in_progress")}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Start Work
          </button>
        )}

        {ticket.status !== "closed" && (
          <button
            onClick={() => onUpdate(ticket.id, "closed")}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Mark Resolved
          </button>
        )}
      </div>
    </div>
  );
}