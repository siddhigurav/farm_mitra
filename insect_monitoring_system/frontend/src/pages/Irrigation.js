import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { AlertTriangle } from 'lucide-react';

export default function Irrigation(){
  const { t } = useTranslation();
  const [enabled, setEnabled] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const toggle = () => {
    setShowConfirm(true);
  }

  const confirm = () => {
    setEnabled(e => !e);
    setShowConfirm(false);
    // TODO: call backend to toggle irrigation
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('irrigation_control')}</h1>
      <div className="bg-white p-4 rounded shadow flex items-center justify-between">
        <div>
          <div className="text-sm text-slate-500">{t('irrigation')}</div>
          <div className="text-xl font-semibold">{enabled ? t('enabled') : t('disabled')}</div>
        </div>
        <div>
          <button onClick={toggle} className={`px-4 py-2 rounded ${enabled ? 'bg-red-500 text-white' : 'bg-green-600 text-white'}`}>{enabled ? t('stop') : t('start')}</button>
        </div>
      </div>

      {showConfirm && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/40">
          <div className="bg-white p-6 rounded shadow w-80">
            <div className="flex items-center gap-2"><AlertTriangle className="text-yellow-500"/> <div className="font-semibold">{t('confirm_action')}</div></div>
            <p className="mt-3 text-sm text-slate-600">{t('confirm_irrigation_text', { action: enabled ? t('stop') : t('start') })}</p>
            <div className="mt-4 flex justify-end gap-2">
              <button className="px-3 py-2" onClick={()=>setShowConfirm(false)}>{t('cancel')}</button>
              <button className="px-3 py-2 bg-blue-600 text-white rounded" onClick={confirm}>{t('confirm')}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
