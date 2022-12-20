import streamlit as st
from streamlit_option_menu import option_menu
import cv2
from PIL import Image
import numpy as np
from deepface import DeepFace
import age_detection
import pandas as pd

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

    with st.sidebar.container():
        logo = Image.open(r'C:\Users\Janika\Downloads\Uni\Data Science\Semester 3\Fallstudie\Logo_nobg1.png')
        cola, colb = st.columns([0.8, 0.2])
        with cola:
            st.markdown(""" <style> .font {
                        font-size:35px ; font-family: 'Eras ITC', 'Eras Light ITC',; color: #ffb166;} 
                        </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Fox Banking</p>', unsafe_allow_html=True)
        with colb:
            st.image(logo)

        choice = option_menu(None, ["Über Uns", "Produktanalyse", "Alle Produkte"],
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
            font-size:35px ; font-family: 'Eras ITC', 'Eras Light ITC',; color: #ffb166;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Fox Banking</p>', unsafe_allow_html=True)
        with col2:  # To display brand log
            st.image(logo, width=130)
        st.write(" Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. ")


    elif choice == "Produktanalyse":
        with st.container():
            st.markdown(""" <style> .font {
                            font-size:35px ; font-family: 'Eras ITC', 'Eras Light ITC',; color: #ffb166;} 
                            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Finde dein perfektes Produkt</p>', unsafe_allow_html=True)
            with st.expander("Wähle ein Bild aus!", expanded=True):
                image_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])
            col1, col2 = st.columns(2)
            with col1:
                if image_file is not None:
                    uploaded_image = Image.open(image_file)
                    st.text("Deine Auswahl")
                    st.image(uploaded_image)
                    nimg = np.array(uploaded_image)
                    cv_image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
            with col2:
                if image_file is not None:
                    with st.spinner("Berechnung"):
                        analyze = analyze_image(uploaded_image)
                        age = age_detection.predict_age(cv_image)
                    st.text(analyze[0])
                    st.text(age)




    elif choice == "Alle Produkte":
        with st.container():
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown(""" <style> .font {
                                            font-size:35px ; font-family: 'Eras ITC', 'Eras Light ITC',; color: #ffb166;} 
                                            </style> """, unsafe_allow_html=True)
                st.markdown('<p class="font">Unsere Produkte im Überblick</p>', unsafe_allow_html=True)

            with col2:
                st.image(logo, width=130)


if __name__ == '__main__':
		main()







# if age = (0,2) or age = (4,6) or age = (8,12) or age = (15,20):


# (including angry, fear, neutral, sad, disgust, happy and surprise)
# AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
#                 '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']












