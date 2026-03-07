import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import CustomerDashboard from "./pages/CustomerDashboard";
import AdminDashboard from "./pages/AdminDashboard";
// ...existing code...
import CreateTicket from "./pages/CreateTicket";
import AgentDashboard from "./pages/AgentDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route path="/customer/create" element={<CreateTicket />} />

        <Route path="/customer" element={<CustomerDashboard />} />

        <Route path="/admin" element={<AdminDashboard />} />

        <Route path="/agent" element={<AgentDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
