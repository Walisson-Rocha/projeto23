import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [detections, setDetections] = useState([]);
  const [processedImage, setProcessedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [manualPlate, setManualPlate] = useState('');
  const [manualResult, setManualResult] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      streamRef.current = stream;
    } catch (err) {
      console.error("Error accessing camera:", err);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const captureAndDetect = async () => {
    if (!videoRef.current || !canvasRef.current) return;
    
    setIsLoading(true);
    
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    
    const imageData = canvas.toDataURL('image/jpeg');
    const blob = await fetch(imageData).then(res => res.blob());
    
    const formData = new FormData();
    formData.append('image', blob, 'capture.jpg');
    
    try {
      const response = await fetch('http://localhost:5000/detect', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      setProcessedImage(`data:image/jpeg;base64,${data.processed_image}`);
      setDetections(data.detections || []);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const checkManualPlate = async () => {
    if (!manualPlate.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/check_plate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ plate: manualPlate }),
      });
      
      const data = await response.json();
      setManualResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sistema de Detecção de Placas</h1>
      </header>
      
      <div className="container">
        <div className="camera-section">
          <div className="video-container">
            <video ref={videoRef} autoPlay playsInline muted></video>
            <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
            {processedImage && (
              <div className="processed-image">
                <img src={processedImage} alt="Processed" />
              </div>
            )}
          </div>
          
          <div className="controls">
            <button onClick={startCamera}>Iniciar Câmera</button>
            <button onClick={stopCamera}>Parar Câmera</button>
            <button onClick={captureAndDetect} disabled={isLoading}>
              {isLoading ? 'Processando...' : 'Detectar Placas'}
            </button>
          </div>
        </div>
        
        <div className="manual-check">
          <h2>Consulta Manual</h2>
          <input
            type="text"
            value={manualPlate}
            onChange={(e) => setManualPlate(e.target.value)}
            placeholder="Digite a placa (ex: ABC1234)"
          />
          <button onClick={checkManualPlate} disabled={isLoading}>
            {isLoading ? 'Consultando...' : 'Consultar DETRAN'}
          </button>
          
          {manualResult && (
            <div className="result">
              <h3>Resultado para: {manualResult.plate}</h3>
              <pre>{JSON.stringify(manualResult.info, null, 2)}</pre>
            </div>
          )}
        </div>
        
        <div className="detections">
          <h2>Placas Detectadas</h2>
          {detections.length > 0 ? (
            <ul>
              {detections.map((detection, index) => (
                <li key={index}>
                  <h3>Placa: {detection.plate}</h3>
                  <div className="vehicle-info">
                    <p><strong>Modelo:</strong> {detection.info.modelo}</p>
                    <p><strong>Marca:</strong> {detection.info.marca}</p>
                    <p><strong>Ano:</strong> {detection.info.ano}</p>
                    <p><strong>Cor:</strong> {detection.info.cor}</p>
                    <p><strong>Situação:</strong> {detection.info.situacao}</p>
                    
                    {detection.info.multas.length > 0 ? (
                      <div className="multas">
                        <h4>Multas:</h4>
                        <ul>
                          {detection.info.multas.map((multa, i) => (
                            <li key={i}>
                              {multa.data} - {multa.infracao} (R$ {multa.valor.toFixed(2)})
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : <p>Nenhuma multa registrada</p>}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p>Nenhuma placa detectada</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;