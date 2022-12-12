import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io
from PIL import Image
import numpy as np
from deepface import DeepFace
import age_detection
# function to load image
try:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
except Exception:
    st.write("Error loading cascade classifiers")

#function for image
def analyze_image(uploaded_image):
    new_image = np.array(uploaded_image.convert('RGB'))  # converting image into array
    image = cv2.cvtColor(new_image, 1)

    emotion = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
    age = DeepFace.analyze(image, actions=['age'], enforce_detection=False)

    emotion = emotion['dominant_emotion']
    age = age['age']

    return emotion, age

def main():
    """Fox Banking Face Detection"""
    st.set_page_config(
        page_title="Fox Banking",
        page_icon="🦊",
        layout="wide",
    )

    choice = option_menu(None, ["Über Uns", "Produktanalyse", "Live Analyse", "Alle Produkte"],
                         icons=["person lines fill", "camera fill","camera reels", "basket"],
                         #menu_icon="app-indicator",
                         default_index=0,
                         orientation="horizontal",
                         styles={
                             "container": {"padding": "5!important", "background-color": "#fafafa"},
                             "icon": {"color": "#ffb166", "font-size": "25px"},
                             "nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#02ab21"},
                         }
                         )

    if choice == "Über Uns":
        st.header("Fox Banking")
        st.text("Janika RULEZZZZZ")

    elif choice == "Produktanalyse":
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                image_file = st.file_uploader("Wähle ein Bild von dir aus", type=['jpg', 'jpeg', 'png'])
                if image_file is not None:
                    uploaded_image = Image.open(image_file)
                    st.text("Deine Auswahl")
                    st.image(uploaded_image)
                    analyze = analyze_image(uploaded_image)
            with col2:
                st.header("Persönlichkeitsanalyse")
                st.subheader("Finde dein perfektes Produkt")
                if image_file is not None:
                    st.text(analyze[0])
                    st.text(analyze[1])


    elif choice == "Live Analyse":
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                picture = st.camera_input("Nimm ein Bild auf")
                if picture is not None:
                    image = Image.open(picture)
                    analyze = analyze_image(image)
            with col2:
                st.header("Webcam Live Analyse")
                if picture is not None:
                    st.text(analyze[0])
                    st.text(analyze[1])


    elif choice == "Alle Produkte":
        st.header("Sparbuch")


if __name__ == '__main__':
		main()