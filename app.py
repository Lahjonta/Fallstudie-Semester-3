import streamlit as st
from streamlit_option_menu import option_menu
import cv2
from PIL import Image
import numpy as np
from deepface import DeepFace
import age_detection
import sqlite3 as sq
import io

#create SQLite Database to store feedback
conn = sq.connect('fox_banking_feedback.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS feedback(age INTEGER, emotion TEXT, product TEXT)")

def add_feedback(age, emotion, product):
    c.execute("INSERT INTO feedback(age, emotion, product) VALUES (?,?,?)", (age, emotion, product))
    conn.commit()


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
    st.set_page_config(
        page_title="Fox Banking",
        page_icon="🦊",
        layout="wide",
    )
    st.markdown(""" <style> .main { font-size:15px}; font-family: 'Eras ITC', 'Eras Light ITC',; color: black;} </style>""", unsafe_allow_html=True)
    st.markdown(""" <style> .font { font-size:35px ; font-family: 'Eras ITC', 'Eras Light ITC',; color: #ffb166;} </style> """, unsafe_allow_html=True)
    st.markdown(""" <style> .sub { font-size:25px}; font-family: 'Eras ITC', 'Eras Light ITC',; color: black;} </style>""", unsafe_allow_html=True)

    with st.sidebar.container():
        logo = Image.open(r'C:\Users\Janika\Downloads\Uni\Data Science\Semester 3\Fallstudie\Logo_nobg1.png')
        cola, colb = st.columns([0.8, 0.2])
        with cola:
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
            st.markdown('<p class="font">Fox Banking</p>', unsafe_allow_html=True)
        with col2:  # To display brand log
            st.image(logo, width=130)
        st.markdown('<p class="main" >Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>', unsafe_allow_html=True)

    elif choice == "Produktanalyse":
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        with col1:
            st.markdown('<p class="font">Finde dein perfektes Produkt</p>', unsafe_allow_html=True)
            with col3:
                with st.expander("Wähle ein Bild aus!", expanded=False):
                    image_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])
                if image_file is not None:
                    uploaded_image = Image.open(image_file)
                    st.text("Deine Auswahl")
                    st.image(uploaded_image)
                    nimg = np.array(uploaded_image)
                    cv_image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
        with col2:
            cola, colb, colc = st.columns(3)
            with colc:
                st.image(logo, width=130)
            with col4:
                if image_file is not None:
                    with st.spinner("Berechnung"):
                        analyze = analyze_image(uploaded_image)
                        age = age_detection.predict_age(cv_image)
                    if (age == '(0, 2)' or age == '(4, 6)' or age == '(8, 12)' or age == '(15, 20)'):
                        if (analyze[0] == 'happy' or analyze[0] == 'neutral'):
                            product = Image.open(r'C:\Users\Janika\Downloads\Uni\Data Science\Semester 3\Fallstudie\Projekt Emotionenerkennung Bank\Produkte\Produktbeschreibung_12.jpg')
                            st.image(product)
                            st.markdown('<p class="font">Dein Produkt: Sparbuch</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist ein Sparbuch?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Das Sparbuch ist ein sehr sicheres, klassisches Sparprodukt von Fox Banking. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Du kannst jederzeit in das Sparbuch einzahlen. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Die Anlage eines Sparbuches ist gebührenfrei. </p>', unsafe_allow_html=True)

                        if (analyze[0] == 'angry' or analyze[0] == 'disgust'):
                            st.markdown('<p class="font">Dein Produkt: Bausparvertrag</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist ein Bausparvertrag?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Ein Bausparvertrag funktioniert in der Sparphase genau wie ein Sparbuch. Nur kann man in der Darlehensphase, die viel später eintritt, sich einen Zins beim Abschluss des Bausparvertrags sichern.</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist die Bausparphase?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> In der Bausparphase spart man so lange ein, bis ein vereinbarter Mindestbetrag eingezahlt wurde. Die Beiträge in den Bausparvertrag werden, wie in einem Sparbuch auch, verzinst angelegt. Wenn der Bausparvertrag zuteilungsreif ist, ist die Bausparkasse verpflichtet, Dir die vorher vereinbarte Darlehenssumme auszuzahlen, die Du nicht in Anspruch nehmen musst. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist die Darlehensphase?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> In der Darlehensphase erhälts Du ein vorher vereinbartes Darlehen zu einem Zins, der beim Abschluss des Bausparvertrags vereinbart wurde. </p>', unsafe_allow_html=True)

                        if (analyze[0] == 'sad'):
                            st.markdown('<p class="font">Dein Produkt: Katastrophenschutz</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist der Katastrophenschutz?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Der Katastrophenschutz sichert die finanzielle Auswirkung von Naturkatastrophen, wie Überschwemmungen, Erdbeben oder Stürme ab. Das können Schäden an Immobilien und anderen Besitztümern sein.</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">   Warum gilt Sie als Zusatzversicherung zur Hausrat- oder Wohngebäudeversicherung?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Naturkatastrophen sind in der genannten Versicherung nicht gesichert. Durch den Zusatzcharakter ist die Versicherung deutliche günstiger als die Hausrat- oder Wohngebäudeversicherung.</p>', unsafe_allow_html=True)

                        if (analyze[0] == 'neutral'):
                            st.markdown('<p class="font">Dein Produkt: Werbegeschenk</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Wenn Du jünger als 21 Jahre bist, erhältst Du, nach einer Einzahlung in Dein Sparbuch ein Werbegeschenk in einem Wert von bis zu 5€! </p>', unsafe_allow_html=True)

                        if (analyze[0] == 'fear' or analyze[0] == 'surprise'):
                            st.markdown('<p class="font">Dein Produkt: Mitgliedschaft </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Als Mitglied und Anteilseigner hast Du ein Stimmrecht bei der Generalversammlung oder bei der Vertreterwahl. Dabei gilt: ein Mitglied, eine Stimme – unabhängig davon, wie viele Geschäftsanteile Du besitzen.</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Du bist dann auch am wirtschaftlichen Erfolg der Fox Bank beteiligt. Du erhältst in der Regel einmal jährliche eine Rendite. Außerdem profitierst Du von exklusiven Mitgliedervorteilen. </p>', unsafe_allow_html=True)

                    if (age == '(25, 32)' or age == '(38, 43)' or age == '(48, 53)'):
                        if (analyze[0] == 'happy' or analyze[0] == 'neutral'):
                            st.markdown('<p class="font">Dein Produkt: Girokonto </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Hier findest Du das passende Girokonto für Dich: </p>', unsafe_allow_html=True)

                            st.markdown('<p class="main"> </p>', unsafe_allow_html=True)

                    st.text(analyze[0])
                    st.text(age)

                    #Feedback form for users
                    st.markdown('<p class="sub">Möchtest Du Feedback geben?</p>', unsafe_allow_html=True)
                    q1 = st.number_input("Wie alt bist Du?", min_value=0, max_value=120)
                    q2 = st.selectbox("Wie würdest Du Deine momentane Emotion beschreiben", (
                    'glücklich', 'neutral', 'wütend', 'traurig', 'angeekelt', 'ängstlich', 'überrascht'))
                    q3 = st.selectbox("Welches Produkt interessiert Dich am meisten?", ('Sparbuch', 'Rechtsschutzversicherung', 'Vermögensberatung', 'Gewinnsparen', 'Sterbegeld- oder Hausratsversicherung', 'Girokonto', 'Kredit', 'Lebensversicherung', 'Aktien', 'Berufsunfähigkeitsversicherung', 'Bausparvertrag', 'Katastrophenschutz', 'Werbegeschenke', 'Mitgliedschaft'))

                    if st.button("Feedback geben"):
                        create_table()
                        add_feedback(q1, q2, q3)
                        st.success("Feedback abgegeben!")


    elif choice == "Alle Produkte":
        with st.container():
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown('<p class="font">Unsere Produkte im Überblick</p>', unsafe_allow_html=True)

            with col2:
                st.image(logo, width=130)


if __name__ == '__main__':
		main()









