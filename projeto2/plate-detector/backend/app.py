from flask import Flask, request, jsonify
from flask_cors import CORS
from detran_api import consultar_detran
import cv2
import numpy as np
import base64
from detector.plate_detector import PlateDetector

app = Flask(__name__)
CORS(app)

detector = PlateDetector()

@app.route('/detect', methods=['POST'])
def detect_plate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    img_bytes = file.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    frame, plate_texts, rects = detector.process_frame(frame)
    
    # Codificar frame processado para resposta
    _, buffer = cv2.imencode('.jpg', frame)
    encoded_frame = base64.b64encode(buffer).decode('utf-8')
    
    # Consultar DETRAN para cada placa detectada
    vehicle_info = []
    for plate in plate_texts:
        info = consultar_detran(plate)
        vehicle_info.append({
            'plate': plate,
            'info': info
        })
    
    return jsonify({
        'processed_image': encoded_frame,
        'detections': vehicle_info,
        'rectangles': rects
    })

@app.route('/check_plate', methods=['POST'])
def check_plate():
    data = request.get_json()
    plate = data.get('plate', '').upper().replace(' ', '')
    
    if not plate or len(plate) < 6:
        return jsonify({'error': 'Placa inválida'}), 400
    
    info = consultar_detran(plate)
    return jsonify({'plate': plate, 'info': info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)