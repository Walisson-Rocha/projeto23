import cv2
import pytesseract
import numpy as np
import re

# Configurações do Tesseract (ajuste o caminho)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def encontrar_placa(img):
    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detectar bordas
    bordas = cv2.Canny(gray, 50, 150)
    
    # Encontrar contornos
    contornos, _ = cv2.findContours(bordas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtar contornos retangulares (placas)
    for cnt in contornos:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:  # Contorno com 4 lados
            x, y, w, h = cv2.boundingRect(cnt)
            proporcao = w / float(h)
            
            # Proporções típicas de placas (BR: ~2:1 ou 3:1)
            if 2.0 < proporcao < 4.0 and w > 100 and h > 30:
                return img[y:y+h, x:x+w]  # Retorna ROI da placa
    
    return None  # Se não encontrar

def ler_placa(roi_placa):
    # Pré-processamento
    gray = cv2.cvtColor(roi_placa, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # OCR
    config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    texto = pytesseract.image_to_string(gray, lang='por+eng', config=config)
    
    # Filtro para placas BR
    padrao = re.compile(r'[A-Z]{3}\d[A-Z0-9]\d{2}|[A-Z]{3}\d{4}')
    return padrao.findall(texto.upper())

# Carregar imagem
img = cv2.imread('carro.jpg')
if img is None:
    print("Erro: Imagem não carregada!")
else:
    # 1. Encontrar região da placa
    placa = encontrar_placa(img)
    
    if placa is not None:
        # 2. Mostrar placa detectada
        cv2.imshow('Placa Detectada', placa)
        cv2.waitKey(0)
        
        # 3. Ler texto da placa
        resultado = ler_placa(placa)
        print("Placa detectada:", resultado[0] if resultado else "Não reconhecida")
    else:
        print("Placa não encontrada na imagem!")

    # Mostrar imagem original (opcional)
    cv2.imshow('Imagem Original', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()