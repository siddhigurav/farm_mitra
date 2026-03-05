import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

export default function Settings() {
  const { t, i18n } = useTranslation();
  const [lang, setLang] = useState(i18n.language || localStorage.getItem('i18nextLng') || 'en');

  useEffect(() => {
    const saved = localStorage.getItem('i18nextLng');
    if (saved && saved !== lang) setLang(saved);
  }, []);

  const changeLang = (newLang) => {
    setLang(newLang);
    i18n.changeLanguage(newLang);
    localStorage.setItem('i18nextLng', newLang);
    document.documentElement.lang = newLang;
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('settings')}</h1>

      <div className="bg-white p-4 rounded shadow dark:bg-slate-800 w-full max-w-md">
        <label className="block text-sm font-medium text-slate-700 mb-2">{t('language') || 'Language'}</label>
        <select value={lang} onChange={(e) => changeLang(e.target.value)} className="w-full p-2 rounded border">
          <option value="en">English</option>
          <option value="hi">हिंदी</option>
          <option value="mr">मराठी</option>
        </select>
      </div>
    </div>
  );
}
