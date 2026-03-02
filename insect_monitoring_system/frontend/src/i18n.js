import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import en from './locales/en/translation.json';
import hi from './locales/hi/translation.json';
import mr from './locales/mr/translation.json';

const resources = {
  en: { translation: en },
  hi: { translation: hi },
  mr: { translation: mr },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    supportedLngs: ['en', 'hi', 'mr'],
    load: 'languageOnly',
    debug: false, // set to true temporarily if you need verbose logs
    interpolation: { escapeValue: false },
    detection: {
      // order and keys for language detection
      order: ['querystring', 'localStorage', 'navigator', 'htmlTag'],
      // ensure we cache to the default localStorage key used by the detector
      caches: ['localStorage'],
      lookupLocalStorage: 'i18nextLng',
    },
    react: {
      useSuspense: false,
    },
  });

// Debugging helper: log the resolved language on init
try {
  console.log('[i18n] initialized, language =', i18n.language);
  i18n.on('languageChanged', (lng) => console.log('[i18n] languageChanged ->', lng));
} catch (e) { /* ignore in non-browser env */ }

export default i18n;
