import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog

import cv2
import easyocr
import matplotlib

matplotlib.use( "TkAgg" )
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

from PIL import Image
from PIL import ImageTk

main_page = tk.Tk()
main_page.configure( bg='#20272d' )
main_page.geometry( "1920x1080" )  # Size of the window
main_page.title( 'OCR' )

add_icon = PhotoImage( file="add64.png" )


def select_image():
    f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'), ('PNG Files', '*.png'), ('SVG Files', '*.svg'),
               ('WebP Files', '*.webp')]
    selected_image = filedialog.askopenfilename( filetypes=f_types )
    img_pillow = Image.open( selected_image )
    img_resized = img_pillow.resize( (255, 255) )
    img1 = ImageTk.PhotoImage( img_resized )
    image_display = tk.Label( main_page, image=img1, borderwidth=0 )
    image_display.image = img1
    image_display.place( x=1100, y=300 )
    cv_img = cv2.imread( selected_image )
    ocr( cv_img )


def ocr(img):
    font = cv2.FONT_HERSHEY_DUPLEX
    reader = easyocr.Reader( ['en'] )
    result = reader.readtext( img )
    spacer = 30
    for detection in result:
        top_left = tuple( detection[0][0] )
        bottom_right = tuple( detection[0][2] )
        text = detection[1]
        img = cv2.rectangle( img, top_left, bottom_right, (0, 255, 0), 2 )
        img = cv2.putText( img, text, (5, spacer), font, 1, (0, 0, 255), 2, cv2.LINE_AA )
        spacer += 30
    f = Figure( figsize=(8, 8), dpi=100 )
    canvas = FigureCanvasTkAgg( f, main_page )
    a = f.add_subplot( 111 )
    a.imshow( img )
    a.axis( 'off' )
    canvas.draw()
    canvas.get_tk_widget().place( x=100, y=10 )


upload_image_btn = tk.Button( main_page, image=add_icon, width=65, height=65, bg='#20272d', fg='#000000',
                              borderwidth=0,
                              command=lambda: select_image() )

upload_image_btn.place( x=1250, y=610 )

main_page.mainloop()  # Keep the window open
