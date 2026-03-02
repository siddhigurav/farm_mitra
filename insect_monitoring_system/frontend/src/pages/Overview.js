import React from 'react';
import { useTranslation } from 'react-i18next';
import useWebSocket from '../hooks/useWebSocket';
import { Thermometer, Droplet, AlertCircle } from 'lucide-react';

const StatCard = ({title, value, icon, color}) => (
  <div className={`p-4 rounded-lg shadow bg-white dark:bg-slate-800 w-full`}> 
    <div className="flex items-center justify-between">
      <div>
        <div className="text-sm text-slate-500">{title}</div>
        <div className="text-2xl font-semibold">{value}</div>
      </div>
      <div className={`p-2 rounded-md ${color}`}>{icon}</div>
    </div>
  </div>
)

export default function Overview(){
  const { t } = useTranslation();
  const { connected, messages } = useWebSocket((window.location.protocol === 'https:' ? 'wss' : 'ws') + '://' + window.location.host + '/ws');
  // derive latest sensor values from messages
  const latestSensor = messages.find(m => m.type === 'sensor') || {};
  const latestVision = messages.find(m => m.type === 'detection') || {};

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{t('overview')}</h1>
        <div className="text-sm text-slate-600">{t('status')}: {connected ? <span className="text-green-600">{t('online')}</span> : <span className="text-red-600">{t('offline')}</span>}</div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard title={t('temperature')} value={latestSensor.dht?.temperature_c ?? '—'} icon={<Thermometer />} color="bg-amber-100 text-amber-600" />
        <StatCard title={t('humidity')} value={latestSensor.dht?.humidity ?? '—'} icon={<Droplet />} color="bg-sky-100 text-sky-600" />
        <StatCard title={t('soil_moisture')} value={latestSensor.soil_percent ?? '—'} icon={<Droplet />} color="bg-green-100 text-green-600" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="col-span-2 p-4 bg-white rounded shadow dark:bg-slate-800">
          <h2 className="font-semibold mb-2">{t('real_time_alerts')}</h2>
          <div className="space-y-2">
            {messages.filter(m=>m.type==='detection').slice(0,10).map((m,i)=> (
              <div key={i} className="p-2 rounded border-l-4 border-red-500 bg-red-50 dark:bg-slate-700"> 
                <div className="text-sm font-medium">{t('animal_detected')}</div>
                <div className="text-xs text-slate-600">{new Date(m.data?.timestamp*1000).toLocaleString()}</div>
              </div>
            ))}
            {messages.filter(m=>m.type==='detection').length===0 && <div className="text-sm text-slate-500">{t('no_alerts')}</div>}
          </div>
        </div>

        <div className="p-4 bg-white rounded shadow dark:bg-slate-800">
          <h2 className="font-semibold mb-2">{t('device_status')}</h2>
          <div className="text-sm text-slate-600">{t('online_devices')}: <strong>{connected ? '1+' : '0'}</strong></div>
        </div>
      </div>
    </div>
  )
}
