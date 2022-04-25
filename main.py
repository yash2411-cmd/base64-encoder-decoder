# from cProfile import label
from cProfile import label
import tkinter as tk
import base64
# from tkinter.tix import COLUMN
from cryptography.fernet import Fernet
from pip import main
root= tk.Tk()
#main frame size
root.geometry("620x420")
root.title("base64 encoder/decoder")

#function for encoding the string into base64 
def base64_encode():
    s= entry1.get()
    s_msg= s.encode("ascii") # converting the string into its ascii values
    base_64_bytes= base64.b64encode(s_msg)  #converting those ascii values in to base64 bytes of 6 bit length
    base_64_msg= base_64_bytes.decode("ascii")  # converting bytes to string encoded message

    label1= tk.Entry(root)
    label1.insert(0,base_64_msg)
    label1.config(font=("mormal",15))
    canvas1.create_window(200,190,window=label1)

# function for decoding the base64 encoded string    
def base64_decode():
    u= entry2.get()
    s_msg= u.encode("ascii")    # converting the base64 string to ascii 
    s_data= base64.b64decode(s_msg) # converting the ascii to 8 bits fromm 6 bits
    main_string= s_data.decode("ascii") # converting the 8 bits to string 

    label2= tk.Entry(root)
    label2.insert(0,main_string)
    label2.config(font=("mormal",15))
    canvas1.create_window(200,320,window=label2)
# def copyencode():
#     pass
# def copydecode():
#     pass

# main windows:

canvas1= tk.Canvas(root,width=400,height=400)
canvas1.pack()

# creating a heading text 
label= tk.Label(root,width=500,height=500,text="Base64 Decoder and Encoder")
label.config(font=("bold",22),bg="#00ccff")
canvas1.create_window(220,60,window=label)

# but3= tk.Button(text="Copy",command=copyencode,bg="#4affb7")
# but4= tk.Button(text="Copy",command=copydecode,bg="#4affb7")

# canvas1.create_window(300,190,window=but3)
# canvas1.create_window(300,320,window=but4)

# entry blocks for user text input 
entry1= tk.Entry(root)
entry1.config(font=("mormal",15))

entry2= tk.Entry(root)
entry2.config(font=("mormal",15))
# putting entry blocks in canvas
canvas1.create_window(200,140,window=entry1)
canvas1.create_window(200,280,window=entry2)

# buttons which are assigned to the function for encode and decode
but1= tk.Button(text="Encode",command=base64_encode,bg="#c20034",fg="#fff")
but2= tk.Button(text="Decode",command=base64_decode,bg="#0f9100",fg="#fff")
but1.config(font=("bold",13))
but2.config(font=("bold",13))

# putting buttons in canvas
canvas1.create_window(400,140,window=but1)
canvas1.create_window(400,280,window=but2)

root.mainloop()
