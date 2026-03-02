import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import useWebSocket from '../hooks/useWebSocket';

function Box({bbox, label}){
  const [x1,y1,x2,y2] = bbox;
  const style = { left: x1, top: y1, width: x2-x1, height: y2-y1 };
  return <div className="absolute border-2 border-red-500" style={style}><div className="text-xs bg-red-500 text-white px-1">{label}</div></div>
}

export default function LiveCamera(){
  const { t } = useTranslation();
  const { messages } = useWebSocket((window.location.protocol === 'https:' ? 'wss' : 'ws') + '://' + window.location.host + '/ws');
  const latestFrameMsg = messages.find(m => m.type === 'frame') || {};
  const detections = latestFrameMsg.data?.detections || [];
  const [imgSrc, setImgSrc] = useState(null);

  useEffect(()=>{
    if(latestFrameMsg.data && latestFrameMsg.data.image_base64){
      setImgSrc('data:image/jpeg;base64,' + latestFrameMsg.data.image_base64)
    }
  }, [latestFrameMsg])

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">{t('live_camera')}</h1>
      <div className="bg-black rounded overflow-hidden relative" style={{maxWidth: '100%', height: 480}}>
        {imgSrc ? (
          <img src={imgSrc} alt="frame" style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-white">{t('no_frame')}</div>
        )}
        {detections.map((d,i)=> <Box key={i} bbox={d.bbox} label={`${d.label} (${Math.round(d.conf*100)}%)`} />)}
      </div>
    </div>
  )
}
