import type { Ticket } from "../types";
import RiskBadge from "./RiskBadge";

export default function TicketCard({ ticket }: { ticket: Ticket }) {
  return (
    <div className="bg-slate-800 p-5 rounded-lg">
      <h3 className="font-semibold text-lg">{ticket.title}</h3>
      <p className="text-slate-400">{ticket.description}</p>

      <div className="flex justify-between mt-3">
        <RiskBadge probability={ticket.breach_probability} />
        <span>Confidence: {(ticket.confidence_score * 100).toFixed(0)}%</span>
      </div>

      {ticket.status === "escalated" && (
        <p className="text-red-400 mt-2">🚨 Escalated</p>
      )}
    </div>
  );
}