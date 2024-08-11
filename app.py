import streamlit as st
import cv2
from PIL import Image
import numpy as np
from google.cloud import vision

# Inicializar cliente de Google Cloud Vision
client = vision.ImageAnnotatorClient()

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
        # Convertir la imagen a bytes para enviar a Google Cloud Vision
        img_byte_arr = cv2.imencode('.jpg', np.array(image))[1].tobytes()
        image = vision.Image(content=img_byte_arr)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            st.subheader("2. TEXTO :")
            st.code(texts[0].description)
        else:
            st.warning("No se detectó texto en la imagen.")
else:
    st.warning("Por favor, sube una imagen o toma una foto para continuar.")
