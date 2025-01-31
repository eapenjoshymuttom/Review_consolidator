import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  RadialBarChart,
  RadialBar,
  PolarGrid,
  PolarRadiusAxis,
  ResponsiveContainer
} from 'recharts';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const ProductRatingsChart = ({ componentRatings, overallRating }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
      {/* Component-wise Ratings */}
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Component Ratings</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={componentRatings}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" className="text-gray-300" />
                <XAxis 
                  type="number" 
                  domain={[0, 5]} 
                  className="text-gray-600"
                />
                <YAxis 
                  dataKey="name" 
                  type="category" 
                  width={100} 
                  className="text-gray-600"
                />
                <Tooltip 
                  formatter={(value) => [`${value} / 5`, 'Rating']}
                  contentStyle={{
                    backgroundColor: 'white',
                    border: '1px solid #ccc',
                    borderRadius: '8px',
                    padding: '8px'
                  }}
                />
                <Bar 
                  dataKey="rating" 
                  fill="#8884d8"
                  radius={[0, 4, 4, 0]}
                  label={{ 
                    position: 'right', 
                    formatter: (value) => `${value}/5`,
                    fill: '#4B5563'
                  }}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Overall Rating */}
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Overall Rating</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart
                innerRadius={80}
                outerRadius={110}
                data={[overallRating]}
                startAngle={90}
                endAngle={-270}
              >
                <PolarGrid radialLines={false} />
                <PolarRadiusAxis
                  angle={90}
                  domain={[0, 5]}
                  tick={false}
                  axisLine={false}
                />
                <RadialBar
                  background
                  dataKey="value"
                  fill="#8884d8"
                  cornerRadius={10}
                  label={{
                    position: 'center',
                    formatter: (value) => `${value}/5`,
                    fontSize: 32,
                    fill: '#1F2937'
                  }}
                />
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProductRatingsChart;