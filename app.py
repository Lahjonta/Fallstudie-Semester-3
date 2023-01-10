import streamlit as st
from streamlit_option_menu import option_menu
import cv2
from PIL import Image
import numpy as np
from deepface import DeepFace
import age_detection
import sqlite3 as sq
import io
import pandas as pd


#create SQLite Database to store feedback
conn = sq.connect('fox_banking.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS feedback(Foto BLOB, Alter_gold INTEGER, Emotion_gold TEXT, Alter_Vorhersage INTEGER, Emotion_Vorhersage TEXT, Produkt TEXT)")

def add_feedback(Foto, Alter_gold, Emotion_gold, Alter_Vorhersage, Emotion_Vorhersage, Produkt):
    c.execute("INSERT INTO feedback(Foto, Alter_gold, Emotion_gold, Alter_Vorhersage, Emotion_Vorhersage, Produkt) VALUES (?,?,?,?,?,?)", (Foto, Alter_gold, Emotion_gold, Alter_Vorhersage, Emotion_Vorhersage, Produkt))
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

    em = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
    global emotion
    emotion = em['dominant_emotion']

    return emotion

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
        logo = Image.open('Logo_nobg1.png')
        cola, colb = st.columns([0.8, 0.2])
        with cola:
            st.markdown('<p class="font">Fox Banking</p>', unsafe_allow_html=True)
        with colb:
            st.image(logo)

        choice = option_menu(None, ["Produktanalyse", "Alle Produkte", "Über Uns"],
                             icons=["camera fill", "basket", "person lines fill"],
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

    logo = Image.open('Fox_banking.png')

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
            st.markdown('<p class="main">Keine Lust mehr auf Berater die dir Produkte verkaufen wollen, die gar nicht zu dir passen? </p>', unsafe_allow_html=True)
            st.markdown('<p class="main">Unser selbst entwickeltes Analysetool bietet dir perfekt passende Produkte an, indem es dein Alter und deine Emotion analysiert. Ganz ohne nervige Beratergespräche.</p>', unsafe_allow_html=True)
            st.markdown('<p class="main">Lade hierfür einfach ein Bild von dir hoch und lass es analysieren:</p>', unsafe_allow_html=True)

            with col3:
                with st.expander("Wähle ein Bild aus!", expanded=False):
                    image_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])
                if image_file is not None:
                    uploaded_image = Image.open(image_file)
                    buf = io.BytesIO()
                    uploaded_image.save(buf, format='PNG')
                    byte_im = buf.getvalue()
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
                        emotion = analyze_image(uploaded_image)
                        age = age_detection.predict_age(cv_image)
                    if (age == '(0, 2)' or age == '(4, 6)' or age == '(8, 12)' or age == '(15, 20)'):
                        if (emotion == 'happy'):
                            st.markdown('<p class="font">Dein Produkt: Sparbuch</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist ein Sparbuch?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Das Sparbuch ist ein sehr sicheres, klassisches Sparprodukt von Fox Banking. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Du kannst jederzeit in das Sparbuch einzahlen. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Die Anlage eines Sparbuches ist gebührenfrei. </p>', unsafe_allow_html=True)

                        if (emotion == 'angry' or emotion == 'disgust'):
                            st.markdown('<p class="font">Dein Produkt: Bausparvertrag</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist ein Bausparvertrag?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Ein Bausparvertrag funktioniert in der Sparphase genau wie ein Sparbuch. Nur kann man in der Darlehensphase, die viel später eintritt, sich einen Zins beim Abschluss des Bausparvertrags sichern.</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist die Bausparphase?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> In der Bausparphase spart man so lange ein, bis ein vereinbarter Mindestbetrag eingezahlt wurde. Die Beiträge in den Bausparvertrag werden, wie in einem Sparbuch auch, verzinst angelegt. Wenn der Bausparvertrag zuteilungsreif ist, ist die Bausparkasse verpflichtet, Dir die vorher vereinbarte Darlehenssumme auszuzahlen, die Du nicht in Anspruch nehmen musst. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist die Darlehensphase?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> In der Darlehensphase erhälts Du ein vorher vereinbartes Darlehen zu einem Zins, der beim Abschluss des Bausparvertrags vereinbart wurde. </p>', unsafe_allow_html=True)

                        if (emotion == 'sad'):
                            st.markdown('<p class="font">Dein Produkt: Katastrophenschutz</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist der Katastrophenschutz?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Der Katastrophenschutz sichert die finanzielle Auswirkung von Naturkatastrophen, wie Überschwemmungen, Erdbeben oder Stürme ab. Das können Schäden an Immobilien und anderen Besitztümern sein.</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">   Warum gilt Sie als Zusatzversicherung zur Hausrat- oder Wohngebäudeversicherung?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Naturkatastrophen sind in der genannten Versicherung nicht gesichert. Durch den Zusatzcharakter ist die Versicherung deutliche günstiger als die Hausrat- oder Wohngebäudeversicherung.</p>', unsafe_allow_html=True)

                        if (emotion == 'neutral'):
                            st.markdown('<p class="font">Dein Produkt: Werbegeschenk</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Wenn Du jünger als 21 Jahre bist, erhältst Du, nach einer Einzahlung in Dein Sparbuch ein Werbegeschenk in einem Wert von bis zu 5€! </p>', unsafe_allow_html=True)

                        if (emotion == 'fear' or emotion == 'surprise'):
                            st.markdown('<p class="font">Dein Produkt: Mitgliedschaft </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Als Mitglied und Anteilseigner hast Du ein Stimmrecht bei der Generalversammlung oder bei der Vertreterwahl. Dabei gilt: ein Mitglied, eine Stimme – unabhängig davon, wie viele Geschäftsanteile Du besitzen.</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Du bist dann auch am wirtschaftlichen Erfolg der Fox Bank beteiligt. Du erhältst in der Regel einmal jährliche eine Rendite. Außerdem profitierst Du von exklusiven Mitgliedervorteilen. </p>', unsafe_allow_html=True)

                    if (age == '(25, 32)' or age == '(38, 43)' or age == '(48, 53)'):
                        if (emotion == 'happy'):
                            st.markdown('<p class="font">Dein Produkt: Girokonto </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main"> Hier findest Du das passende Girokonto für Dich: </p>', unsafe_allow_html=True)
                            gTable = pd.read_csv("Girokonto.txt", sep="\t")
                            hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                            st.markdown(hide_table_row_index, unsafe_allow_html=True)
                            st.table(gTable)

                        if (emotion == 'angry' or emotion == 'disgust'):
                            st.markdown('<p class="font">Dein Produkt: Kredit</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Warum ein Kredit bei der Fox Bank </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Wir unterstützen dich mit unseren individuellen Krediten dabei, größere Anschaffungen zu realisieren und deine Wünsche Wirklichkeit werden zu lassen – egal, ob eine neue Einrichtung, ein größeres Auto oder eine neue Wohnung. Mit unserem Kreditrechner berechnest du direkt online die monatliche Rate für deinen Wunschkredit. </p>', unsafe_allow_html=True)
                        
                        if (emotion == 'sad'):
                            st.markdown('<p class="font">Dein Produkt: Lebensversicherung</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist eine Lebensversicherung?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Die Lebensversicherung dient an erster Stelle als Hinterbliebenschutz. Falls der Todesfall des Versicherten eintritt, wird den Hinterbliebenen eine vereinbarte Summe ausgezahlt. </p>', unsafe_allow_html=True)
                        
                        if (emotion == 'neutral'):
                            st.markdown('<p class="font">Dein Produkt: Aktien</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Wenn du auf der Suche nach einer renditestarken Anlage sind und bereit sind, ein Risiko einzugehen, sind Aktien sicher von Interesse für dich. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Die Fox Bank hat hochqualifizierte Wertpapier-SpezialistInnen, die dich gerne über die Aktien beraten möchte. </p>', unsafe_allow_html=True)

                        if (emotion == 'fear' or emotion == 'surprise'):
                            st.markdown('<p class="font">Dein Produkt: Berufsunfähigkeitsversicherung</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist die Berufsunfähigkeitsversicherung? </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Wenn du arbeitsunfähig wirst und deinen Beruf aus gesundheitlichen Gründen nicht mehr ausüben können, kannst du deinen Lebensstandard nicht mehr aufrechterhalten, weil dir das Einkommen fehlt. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Die Berufsunfähigkeitsversicherung leistet dir dann monatlichen einen Beitrag, um diese Lücke zu schließen, falls die Arbeitsunfähigkeit eintritt. </p>', unsafe_allow_html=True)

                    if (age == '(60, 100)'):
                        if (emotion == 'happy'):
                            st.markdown('<p class="font">Dein Produkt: Für die Enkel sparen </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Sorge für deine Liebsten vor </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">Speziell für Neu¬geborene und Kinder bis 8 Jahre gibt es das Enkelsparprogramm. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Regelmäßig sparen </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">Mit Beträgen zwischen mindestens 25 Euro und maximal 250 Euro kannst du regelmäßig in dieses Programm einzahlen. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Keine Gebühren </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">Dieses Konto ist bis zum 18. Geburtstag deines Enkels kostenfrei. </p>', unsafe_allow_html=True)
                            SparTable = pd.read_csv("EnkelSparen.txt", sep="\t")
                            hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                            st.markdown(hide_table_row_index, unsafe_allow_html=True)
                            st.table(SparTable)

                        if (emotion == 'angry' or emotion == 'disgust'):
                            st.markdown('<p class="font">Dein Produkt: Rechtsschutzversicherung</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist eine Rechtsschutzversicherung? </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Deckt Kosten für rechtliche Auseinandersetzungen ab</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Z.B Kosten für das Gerichtsverfahren oder Anwaltskosten </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Gebühren: Angebote schon für 10€ im Monat</p>', unsafe_allow_html=True)
                       
                        if (emotion == 'sad'):
                            st.markdown('<p class="font">Dein Produkt: Vermögensberatung</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist eine Vermögensberatung?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Optimierung und Analyse von Vermögenswerten </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Buche einen Termin mit deine(r) BeraterIn und hole ein unverbindliches Angebot</p>', unsafe_allow_html=True)
                        
                        if (emotion == 'neutral'):
                            st.markdown('<p class="font">Dein Produkt: Gewinnsparen</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Wie funktioniert Gewinnsparen? </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Clevere Kombination aus Gewinnen, Sparen und Helfen </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Der monatliche Los Preis beträgt 5€, wobei 4€ gespart werden. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was kann ich gewinnen?</p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Mit dem einem Euro nimmst du an der Verlosung teil. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Neben attraktiven Geldpreisen werden auch Sachpreise wie zum Beispiel Autos und Reisen verlost. </p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist eine Soziallotterie? </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Je Los fließen pro Monat 25 Cent an gemeinnützige Zwecke </p>', unsafe_allow_html=True)
                        
                        if (emotion == 'fear' or emotion == 'surprise'):
                            st.markdown('<p class="font">Dein Produkt: Sterbegeld</p>', unsafe_allow_html=True)
                            st.markdown('<p class="sub">Was ist die Sterbegeldversicherung? </p>', unsafe_allow_html=True)
                            st.markdown('<p class="main">  Im Todesfall eines Versicherten wird eine festgelegte Summe an den Hinterbliebenen ausgezahlt. Diese Auszahlung soll die Bestattungskosten decken. </p>', unsafe_allow_html=True)
                            
                    st.write("")
                    st.write("")
                    st.write("")
                    #Feedback form for users
                    st.markdown('<p class="sub">Möchtest Du Feedback geben?</p>', unsafe_allow_html=True)
                    q1 = st.number_input("Wie alt bist Du?", min_value=0, max_value=120)
                    q2 = st.selectbox("Wie würdest Du Deine momentane Emotion beschreiben", (
                    'glücklich', 'neutral', 'wütend', 'traurig', 'angeekelt', 'ängstlich', 'überrascht'))
                    q3 = st.selectbox("Welches Produkt interessiert Dich am meisten?", ('Sparbuch', 'Rechtsschutzversicherung', 'Vermögensberatung', 'Gewinnsparen', 'Sterbegeld- oder Hausratsversicherung', 'Girokonto', 'Kredit', 'Lebensversicherung', 'Aktien', 'Berufsunfähigkeitsversicherung', 'Bausparvertrag', 'Katastrophenschutz', 'Werbegeschenke', 'Mitgliedschaft'))

                    if st.button("Feedback geben"):
                        create_table()
                        if emotion == 'happy':
                            x = 'glücklich'
                        elif emotion == 'angry':
                            x = 'wütend'
                        elif emotion == 'disgust':
                            x = 'angeekelt'
                        elif emotion == 'sad':
                            x = 'traurig'
                        elif emotion == 'neutral':
                            x = 'neutral'
                        elif emotion == 'fear':
                            x = 'ängstlich'
                        elif emotion == 'surprised':
                            x = 'überrascht'
                        add_feedback(byte_im, q1, q2, age, x, q3)
                        st.success("Feedback abgegeben!")

        with col1:
            with col3:
                if image_file is not None:
                    if emotion == 'happy':
                        x = 'glücklich'
                    elif emotion == 'angry':
                        x = 'wütend'
                    elif emotion == 'disgust':
                        x = 'angeekelt'
                    elif emotion == 'sad':
                        x = 'traurig'
                    elif emotion == 'neutral':
                        x = 'neutral'
                    elif emotion == 'fear':
                        x = 'ängstlich'
                    elif emotion == 'surprised':
                        x = 'überrascht'

                    if (age == '(0, 2)' or age == '(4, 6)' or age == '(8, 12)' or age == '(15, 20)'):
                        a = 'ein Kind'
                    if (age == '(25, 32)' or age == '(38, 43)' or age == '(48, 53)'):
                        a = 'Erwachsen'
                    if (age == '(60, 100)'):
                        a = 'eine ältere Person'
                    st.markdown('<p class="main">Laut unserer Bildanalyse bist du {} und {}. </p>'.format(x, a), unsafe_allow_html=True)




    elif choice == "Alle Produkte":
        with st.container():
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown('<p class="font">Unsere Produkte im Überblick</p>', unsafe_allow_html=True)

            with col2:
                st.image(logo, width=130)


if __name__ == '__main__':
		main()









