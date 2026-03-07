export default function RiskBadge({ probability }: { probability: number }) {
  let color = "bg-green-500";

  if (probability > 0.8) color = "bg-red-500";
  else if (probability > 0.6) color = "bg-orange-500";
  else if (probability > 0.4) color = "bg-yellow-500";

  return (
    <span className={`${color} px-3 py-1 rounded text-sm`}>
      {(probability * 100).toFixed(0)}%
    </span>
  );
}