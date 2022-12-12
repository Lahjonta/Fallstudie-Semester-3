# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:49:46 2022

@author: Janika
"""
from deepface import DeepFace
from tkinter import filedialog as fd
import tkinter as tk
import time

# Function to open an Image for analysis
def select_file():
    root = tk.Tk()
    root.withdraw()
    filetypes = (
        ('jpg', '*.jpg'),
        ('jpeg', '*.jpeg'),
        ('All Files', '*.*')
    )

    path = fd.askopenfilename(
        title="Select a picture",
        initialdir=r'C:\Users',
        filetypes=filetypes
    )

    return path

start_time = time.time()
# Analyze the selected image
try:
    def analysis():
        image = select_file()
        emotion = DeepFace.analyze(image, actions=['emotion'])
        age = DeepFace.analyze(image, actions=['age'])
        print(emotion['dominant_emotion'])
        print(age)


    analysis()

except:
    print('Please choose a valid image File')

print("--- %s seconds ---" % (time.time() - start_time))
