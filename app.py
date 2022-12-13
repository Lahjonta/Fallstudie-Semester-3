import streamlit as st
from streamlit_option_menu import option_menu
import cv2
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
    age = age["age"]

    return emotion, age

def main():
    """Fox Banking Face Detection"""
    st.set_page_config(
        page_title="Fox Banking",
        page_icon="🦊",
        layout="wide",
    )

    with st.sidebar:
        choice = option_menu(None, ["Über Uns", "Produktanalyse", "Live Analyse", "Alle Produkte"],
                             icons=["person lines fill", "camera fill","camera-reels", "basket"],
                             #menu_icon="app-indicator",
                             default_index=0,
                             styles={
                                 "container": {"padding": "5!important", "background-color": "#fafafa"},
                                 "icon": {"color": "#ffb166", "font-size": "25px"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px",
                                              "--hover-color": "#eee"},
                                 "nav-link-selected": {"background-color": "#02ab21"},
                             }
                             )

    logo = Image.open(r'C:\Users\Janika\Downloads\Uni\Data Science\Semester 3\Fallstudie\Fox_banking.png')
    if choice == "Über Uns":
        col1, col2 = st.columns([0.8, 0.2])
        with col1:  # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #ffb166;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)
        with col2:  # To display brand log
            st.image(logo, width=130)


    elif choice == "Produktanalyse":
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                image_file = st.file_uploader("Wähle ein Bild von dir aus", type=['jpg', 'jpeg', 'png'])
                if image_file is not None:
                    uploaded_image = Image.open(image_file)
                    #convert PIL.Image to cv2.imread type??
                    st.text("Deine Auswahl")
                    st.image(uploaded_image)
                    nimg = np.array(uploaded_image)
                    cv_image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
            with col2:
                st.markdown(""" <style> .font {
                                            font-size:35px ; font-family: 'Cooper Black'; color: #ffb166;} 
                                            </style> """, unsafe_allow_html=True)
                st.markdown('<p class="font">Persönlichkeitsanalyse</p>', unsafe_allow_html=True)
                if image_file is not None:
                    with st.spinner("Berechnung"):
                        analyze = analyze_image(uploaded_image)
                        age = age_detection.predict_age(cv_image)
                    st.text(analyze[0])
                    st.text(age)


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