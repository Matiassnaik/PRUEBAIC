import streamlit as st
import openai
from PIL import Image
import io
import base64
# Poné tu API KEY acá
OPENAI_API_KEY = OPENAI_API_KEY = "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"

st.set_page_config(page_title="Análisis de Placas Insectocaptores", layout="centered")
st.title("Análisis de Placas de Insectocaptor")
st.write("Subí una foto de la placa, o sacala en vivo, para analizar la saturación y los tipos de insectos.")

openai.api_key = OPENAI_API_KEY

# Subir imagen o tomar foto
img_file = st.file_uploader("Elegí una foto o sacala en vivo", type=["jpg", "jpeg", "png"])

if img_file:
    # Mostrar la imagen subida
    img = Image.open(img_file)
    st.image(img, caption="Imagen seleccionada", use_column_width=True)
    
    # Convertir la imagen a base64 para enviar a OpenAI
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    st.info("Analizando...")

    # Prompt que se le envía a GPT-4o
    prompt = (
        "Analiza la siguiente imagen de una placa de insectocaptor. "
        "Devuelve el porcentaje estimado de saturación de la placa (porcentaje de superficie ocupada por insectos). "
        "Luego, dentro de ese porcentaje de saturación, divide y estima qué porcentaje corresponde a cada tipo de insecto visible (ejemplo: moscas, polillas, otros). "
        "Responde SOLO con un resumen numérico en este formato:\n\n"
        "Saturación total: X%\n"
        "Moscas: Y% de la saturación\n"
        "Polillas: Z% de la saturación\n"
        "Otros: W% de la saturación\n"
        "Cantidad total de insectos: N\n"
        "No incluyas texto explicativo adicional."
    )

    # Llamada a la API de OpenAI Vision
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/png;base64,{img_base64}"},
                ],
            }
        ],
        max_tokens=300
    )

    # Mostrar el resultado
    st.success("Resultado del análisis:")
    st.code(response.choices[0].message.content)
    st.caption("Desarrollado por ChatGPT & Matías")

else:
    st.info("Por favor, subí una foto o sacala en vivo para comenzar.")

