import streamlit as  st
from PIL import Image

import pandas as pd

d = {'': ['Kontoführung', 'Überweisung', '', '', '', 'Lastschrift oder Gutschrift einer Überweisung', 'Bargeldauszahlung', 'Bargeldauszahlung mit einer Debitkarte am Geldautomaten', 'Bargeldeinzahlung', '', '', 'Kontoauszüge', '', 'Ausgabe einer Debitkarte', 'Ausgabe einer Kreditkarte'],
     '': ['pro Monat', 'online', 'online Echtzeit-Überweisung', 'SB-Terminal', 'beleghaft, telefonisch', 'beleglos', 'Schalter', 'girocard maestro im BankCard ServiceNetz', 'Schalter', 'Münzen im Safebag am Schalter', 'Geldautomat (girocard maestro im BankCard ServiceNetz)','digital - PDF im elektronischen Postfach 10 Jahre sicher und bequem abrufbar', 'SB-Terminal', 'girocard maestro (Kontoinhaber/Mitkontoinhaber)', 'Rabatt wird auf die erste Kreditkarte pro Kontoinhaber berechnet'],
     'Girokonto [€]': [3.49, 0,0.29,0.09,1.99,0.09,1.99,0, '2 x pro Monat inkl. danach jeweils 1,99 Euro', '1 x pro Monat inkl. danach jeweils 4,99 Euro', 0,0, '1 x pro Monat inkl. danach jeweils 0,19 Euro',0,'']
     }

df = pd.DataFrame(data = d)
df




