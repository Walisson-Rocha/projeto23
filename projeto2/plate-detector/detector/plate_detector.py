import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

class PlateDetector:
    def __init__(self):
        self.plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
        self.min_area = 500
        
    def detect_plates(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = self.plate_cascade.detectMultiScale(gray, 1.1, 4)
        
        plate_imgs = []
        plate_rects = []
        
        for (x, y, w, h) in plates:
            area = w * h
            if area > self.min_area:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                plate_img = frame[y:y+h, x:x+w]
                plate_imgs.append(plate_img)
                plate_rects.append((x, y, w, h))
                
        return frame, plate_imgs, plate_rects
    
    def preprocess_plate(self, plate_img):
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        return invert
    
    def read_plate_text(self, processed_plate):
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text = pytesseract.image_to_string(processed_plate, config=custom_config)
        text = re.sub(r'[^A-Z0-9]', '', text)
        return text.strip()
    
    def process_frame(self, frame):
        frame, plates, rects = self.detect_plates(frame.copy())
        plate_texts = []
        
        for plate in plates:
            processed = self.preprocess_plate(plate)
            text = self.read_plate_text(processed)
            if len(text) >= 6:  # Mínimo de caracteres para uma placa
                plate_texts.append(text)
                
        return frame, plate_texts, rects