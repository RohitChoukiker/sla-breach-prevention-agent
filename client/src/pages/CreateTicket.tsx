import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CreateTicket() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [urgency, setUrgency] = useState("low");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title || !description) {
      alert("Please fill all fields");
      return;
    }

    setLoading(true);

    // Demo delay (simulate API)
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);

      // Redirect after 1.5 sec
      setTimeout(() => {
        navigate("/customer");
      }, 1500);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="bg-white w-full max-w-2xl p-10 rounded-2xl shadow-lg">

        {/* Header */}
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Create New Ticket
        </h1>
        <p className="text-gray-500 mb-8">
          Submit your issue and our AI will predict SLA breach risk.
        </p>

        {success ? (
          <div className="bg-green-100 text-green-700 p-4 rounded-lg">
            ✅ Ticket created successfully! Redirecting...
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">

            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Ticket Title
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                placeholder="e.g. Production server not responding"
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                rows={5}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                placeholder="Describe the issue in detail..."
              />
            </div>

            {/* Urgency */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Urgency Level
              </label>
              <select
                value={urgency}
                onChange={(e) => setUrgency(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 rounded-lg font-semibold transition ${
                loading
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-indigo-600 hover:bg-indigo-700 text-white"
              }`}
            >
              {loading ? "Submitting..." : "Submit Ticket"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}