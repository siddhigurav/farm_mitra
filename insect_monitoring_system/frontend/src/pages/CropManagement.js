import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

const pesticides = [
  { crop: 'Grapes', suggestions: ['Pesticide A', 'Pesticide B'] },
  { crop: 'Wheat', suggestions: ['Pesticide X'] }
]

export default function CropManagement(){
  const { t } = useTranslation();
  const [crops, setCrops] = useState([]);
  const [name, setName] = useState('');

  const add = () => { if(name.trim()){ setCrops(c=>[...c, {name, stage: t('seedling'), added: Date.now()}]); setName(''); } }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('crop_management')}</h1>
      <div className="bg-white p-4 rounded shadow mb-4">
        <div className="flex gap-2">
          <input className="border rounded p-2 flex-1" placeholder={t('crop_name_placeholder')} value={name} onChange={e=>setName(e.target.value)} />
          <button className="px-4 py-2 bg-green-600 text-white rounded" onClick={add}>{t('add_crop')}</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {crops.map((c,i)=> (
          <div key={i} className="bg-white p-4 rounded shadow">
            <div className="font-semibold text-lg">{c.name}</div>
            <div className="text-sm text-slate-600">{t('stage')}: {c.stage}</div>
            <div className="mt-2 text-sm">{t('suggested_pesticides')}:</div>
            <ul className="text-sm list-disc ml-5">
              {(pesticides.find(p=>p.crop.toLowerCase()===c.name.toLowerCase())?.suggestions || [t('no_data')]).map((s,idx)=>(<li key={idx}>{s}</li>))}
            </ul>
          </div>
        ))}
        {crops.length===0 && <div className="text-slate-500">{t('no_crops')}</div>}
      </div>
    </div>
  )
}
