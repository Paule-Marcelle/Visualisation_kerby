import streamlit as st
import fitz  # PyMuPDF
import base64
from io import BytesIO
import os

def convert_pdf_to_images(pdf_path, zoom=2):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        mat = fitz.Matrix(zoom, zoom)  # Augmente la résolution de l'image
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes()
        img_data = BytesIO(img_bytes)
        images.append(img_data)
    return images

def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.title("VISUALISATION DES DONNEES KERBY")

    # Définir l'image de fond (optionnel)
    set_background("C:/Users/bmd tech/deploy_kerby/image4.jpg")

    # Chemins vers les fichiers PDF
    pdf_dir = "C:/Users/bmd tech/deploy_kerby"
    pdf_files = {
        "DATA March & April 2024": os.path.join(pdf_dir, "Data Analysis March&April2024.pdf"),
        "DATA May 2024": os.path.join(pdf_dir, "Data Analysis_MAY2024.pdf")
    }

    # Sélection du fichier PDF
    pdf_choice = st.selectbox("Choisissez le Rapport à visualiser :", list(pdf_files.keys()))
    pdf_path = pdf_files[pdf_choice]

    # Précharger les images si le fichier PDF change
    if 'images' not in st.session_state or st.session_state.pdf_path != pdf_path:
        st.session_state.images = convert_pdf_to_images(pdf_path, zoom=2)  # Utiliser un zoom de 2 pour une meilleure résolution
        st.session_state.page_number = 0
        st.session_state.pdf_path = pdf_path

    # Afficher l'image actuelle
    st.image(st.session_state.images[st.session_state.page_number], use_column_width=True)

    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Page Précédente"):
            if st.session_state.page_number > 0:
                st.session_state.page_number -= 1

    with col3:
        if st.button("Page Suivante"):
            if st.session_state.page_number < len(st.session_state.images) - 1:
                st.session_state.page_number += 1

    # Afficher le numéro de la page
    st.write(f"Page {st.session_state.page_number + 1} sur {len(st.session_state.images)}")

if __name__ == "__main__":
    main()
