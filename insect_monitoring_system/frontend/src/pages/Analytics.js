import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, TimeScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js';
ChartJS.register(TimeScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

function sampleSeries(points=24){
  const labels = Array.from({length: points}).map((_,i)=> new Date(Date.now() - (points-i)*3600*1000));
  const data = labels.map(()=> Math.random()*40 + 10);
  return { labels, data };
}

import { useTranslation } from 'react-i18next';

export default function Analytics(){
  const { t } = useTranslation();
  const temp = sampleSeries(24);
  const moisture = sampleSeries(24);
  const chartData = {
    labels: temp.labels,
    datasets: [
      { label: 'Temperature (C)', data: temp.data, borderColor: 'rgb(255,99,71)', tension: 0.3 },
      { label: 'Soil moisture (%)', data: moisture.data, borderColor: 'rgb(99, 102, 241)', tension: 0.3 }
    ]
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('analytics')}</h1>
      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-2">{t('last_24_hours')}</h2>
        <Line data={chartData} />
      </div>
    </div>
  )
}
