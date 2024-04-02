import tkinter as tk
from tkinter import messagebox
import base64
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
from Crypto.Cipher import DES, DES3, PKCS1_OAEP, Blowfish
from Crypto.PublicKey import RSA
import hashlib
import webbrowser

def perform_action():
    action = selected_action.get()
    if action == "Encode":
        encode_data()
    elif action == "Decode":
        decode_data()
    else:
        show_message("Invalid action selected")

def encode_data():
    data = entry1.get().encode("utf-8")
    algorithm = selected_algorithm.get()
    
    if algorithm == "Base64":
        result = base64.b64encode(data).decode("utf-8")
    elif algorithm == "AES":
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        result = base64.b64encode(encrypted_data).decode("utf-8")
    elif algorithm == "DES":
        des = DES.new(b'abcdefgh', DES.MODE_ECB)
        padded_data = data + b"\0" * (8 - len(data) % 8)  
        encrypted_data = des.encrypt(padded_data)
        result = base64.b64encode(encrypted_data).decode("utf-8")
    elif algorithm == "3DES":
        des3 = DES3.new(b'abcdefghabcdefgh', DES3.MODE_ECB)
        padded_data = data + b"\0" * (8 - len(data) % 8)  
        encrypted_data = des3.encrypt(padded_data)
        result = base64.b64encode(encrypted_data).decode("utf-8")
    elif algorithm == "RSA":
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
        encrypted_data = cipher.encrypt(data)
        result = base64.b64encode(encrypted_data).decode("utf-8")
    elif algorithm == "Blowfish":
        key = b'Sixteen byte key'
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        padded_data = data + b"\0" * (8 - len(data) % 8)  
        encrypted_data = cipher.encrypt(padded_data)
        result = base64.b64encode(encrypted_data).decode("utf-8")
    elif algorithm == "XOR":
        xor_key = hashlib.sha256(b'my_secret_key').digest()[:16]  # Use a 16-byte key for XOR
        encrypted_data = bytes([data[i] ^ xor_key[i % len(xor_key)] for i in range(len(data))])
        result = base64.b64encode(encrypted_data).decode("utf-8")
    else:
        result = "Invalid algorithm selected"
    
    label_result.delete(0, tk.END)  
    label_result.insert(0, result)
    show_message("Encoding successful!")

def decode_data():
    data = entry1.get()
    algorithm = selected_algorithm.get()
    
    try:
        decoded_data = base64.b64decode(data)
        if algorithm == "Base64":
            result = decoded_data.decode("utf-8")
        elif algorithm == "AES":
            key = Fernet.generate_key()
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(decoded_data)
            result = decrypted_data.decode("utf-8")
        elif algorithm == "DES":
            des = DES.new(b'abcdefgh', DES.MODE_ECB)
            decrypted_data = des.decrypt(decoded_data)
            # Remove padding
            result = decrypted_data.rstrip(b"\0").decode("utf-8")
        elif algorithm == "3DES":
            des3 = DES3.new(b'abcdefghabcdefgh', DES3.MODE_ECB)
            decrypted_data = des3.decrypt(decoded_data)
            # Remove padding
            result = decrypted_data.rstrip(b"\0").decode("utf-8")
        elif algorithm == "RSA":
            key = RSA.generate(2048)
            private_key = key.export_key()
            cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
            decrypted_data = cipher.decrypt(decoded_data)
            result = decrypted_data.decode("utf-8")
        elif algorithm == "Blowfish":
            key = b'Sixteen byte key'
            cipher = Blowfish.new(key, Blowfish.MODE_ECB)
            decrypted_data = cipher.decrypt(decoded_data)
            # Remove padding
            result = decrypted_data.rstrip(b"\0").decode("utf-8")
        elif algorithm == "XOR":
            xor_key = hashlib.sha256(b'my_secret_key').digest()[:16]  # Use a 16-byte key for XOR
            decrypted_data = bytes([decoded_data[i] ^ xor_key[i % len(xor_key)] for i in range(len(decoded_data))])
            result = decrypted_data.decode("utf-8")
        else:
            result = "Invalid algorithm selected"
        
        label_result.delete(0, tk.END)  
        label_result.insert(0, result)
        show_message("Decoding successful!")
    except Exception as e:
        label_result.delete(0, tk.END)
        label_result.insert(0, "Error decoding data")
        show_message(str(e))

def show_message(message):
    messagebox.showinfo("Message", message)

def open_link():
    webbrowser.open("https://www.python.org/")

root = tk.Tk()
root.title("Encoder/Decoder")

# Load and resize background image
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas for background image
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill=tk.BOTH, expand=tk.YES)

# Place the background image on the canvas with opacity
canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)
canvas.create_rectangle(0, 0, root.winfo_screenwidth(), root.winfo_screenheight(), fill="black", stipple='gray50')

# Create a frame to hold the widgets
frame = tk.Frame(canvas, bg='white', bd=5)
frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor='center')

# Place widgets inside the frame
label_title = tk.Label(frame, text="Encoder/Decoder", font=("Arial", 24))
label_title.pack(pady=10)

entry1 = tk.Entry(frame, width=50, font=("Arial", 12))
entry1.pack(pady=10)

selected_algorithm = tk.StringVar()
selected_algorithm.set("Base64")  # Default algorithm
algorithms = ["Base64", "AES", "DES", "3DES", "RSA", "Blowfish", "XOR"]
option_menu_algorithm = tk.OptionMenu(frame, selected_algorithm, *algorithms)
option_menu_algorithm.config(font=("Arial", 12))
option_menu_algorithm.pack(pady=10)

selected_action = tk.StringVar()
selected_action.set("Encode")  # Default action
actions = ["Encode", "Decode"]
option_menu_action = tk.OptionMenu(frame, selected_action, *actions)
option_menu_action.config(font=("Arial", 12))
option_menu_action.pack(pady=10)

button_perform = tk.Button(frame, text="Perform Action", command=perform_action, bg="#4CAF50", fg="white", font=("Arial", 14))
button_perform.pack(pady=10)

label_result = tk.Entry(frame, width=50, font=("Arial", 12))
label_result.pack(pady=10)

button_link = tk.Button(frame, text="Learn more", command=open_link, bg="#2196F3", fg="white", font=("Arial", 12))
button_link.pack(pady=10)

# Configure resizing behavior
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
