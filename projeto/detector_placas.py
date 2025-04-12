import re
import cv2
import pytesseract
import os

# ===== CONFIGURAÇÕES TESSERACT =====
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'  # Adicione esta linha

# ===== FUNÇÃO DETECTAR PLACA =====
def detectar_placa(imagem_path):
    try:
        img = cv2.imread(imagem_path)
        if img is None:
            return "Erro: Falha ao carregar imagem"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Usa 'por' ou fallback para 'eng'
        try:
            texto = pytesseract.image_to_string(gray, lang='por', config='--psm 6')
        except:
            texto = pytesseract.image_to_string(gray, lang='eng', config='--psm 6')
        
        padrao_placa = re.compile(r'[A-Z]{3}\d[A-Z0-9]\d{2}|[A-Z]{3}\d{4}')
        placas = padrao_placa.findall(texto.upper())
        
        return placas[0] if placas else "Nenhuma placa detectada"
    
    except Exception as e:
        return f"Erro: {str(e)}"

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    IMAGEM_PATH = r"C:\Users\walis\Downloads\projeto23\projeto\Placa carro - Imgur.jpg"
    resultado = detectar_placa(IMAGEM_PATH)
    print("Resultado:", resultado)