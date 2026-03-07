export type Role = "customer" | "agent" | "admin";

export interface User {
  id: string;
  email: string;
  role: Role;
  token: string;
}

export interface Ticket {
  id: string;
  title: string;
  description: string;
  urgency_requested: string;
  breach_probability: number;
  confidence_score: number;
  priority_final: string;
  status: string;
}