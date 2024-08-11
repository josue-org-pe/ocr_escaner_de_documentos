import streamlit as st
from PIL import Image, ImageOps
import pytesseract
import numpy as np

# Configuración de pytesseract (solo si usas Tesseract)
# pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'

st.markdown("<h1 style='text-align: center;'>ESCÁNER DE DOCUMENTOS</h1>", unsafe_allow_html=True)

# MODO DE SUBIR LA FOTO
col1, col2, col3 = st.columns([2, 3, 4])
col1.subheader("1. MODO")
with col2:
    modo = st.selectbox("", ("SUBE TU IMAGEN", "USAR CAMARA"))

imagen = None
picture = None
with col3:
    if modo == "SUBE TU IMAGEN":
        imagen = st.file_uploader("", type=["png", "jpg", "jpeg"])
    elif modo == "USAR CAMARA":
        picture = st.camera_input("Toma una foto")

image = None
if imagen is not None:
    image = Image.open(imagen)
elif picture is not None:
    image = Image.open(picture)

if image is not None:
    if st.button("ESCANEAR"):
        st.image(image, caption="", use_column_width=True)
        
        # Convertir la imagen a escala de grises
        gray_image = ImageOps.grayscale(image)
        
        # Convertir la imagen a un formato que pytesseract pueda procesar
        thresh_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')
        
        # Usar pytesseract para extraer texto
        text = pytesseract.image_to_string(thresh_image)
        
        st.subheader("2. TEXTO :")
        st.code(text)
else:
    st.warning("Por favor, sube una imagen o toma una foto para continuar.")
