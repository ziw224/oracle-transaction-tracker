// chart 1 is for the transaction amount in number
import "./chart1.css";
// Go to https://recharts.org/en-US/api for more information about making charts
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "January", Total: 1200 },
  { name: "February", Total: 2100 },
  { name: "March", Total: 1000 },
  { name: "April", Total: 3000 },
  { name: "May", Total: 2000 },
  { name: "June", Total: 1500 },
];

export const Chart1 = () => {
  return (
    <div className="chart">
      <div className="chart-title"> Last 6 Months (Overall Transaction in Number)</div>
      <ResponsiveContainer width="100%" aspect={2 / 1}>
        <LineChart
          width={730}
          height={250}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="Total"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
