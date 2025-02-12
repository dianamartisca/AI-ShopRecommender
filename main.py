import os
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

with open('app/resources/data.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

def load_image(file_path, x, y):
	try:
		if not os.path.exists(file_path):
			print(f"Eroare: Fișierul {file_path} nu există.")
			return None

		image = Image.open(file_path)
		image = image.resize((x, y), Image.LANCZOS)
		return ImageTk.PhotoImage(image)
	except Exception as e:
		print(f"Eroare la încărcarea imaginii: {e}")
		return None

def add_to_cart(product_name, category, products):
    """ Display a pop-up when a product is added to the cart, along with recommended products. """
    popup = tk.Toplevel()
    popup.title("Added to Cart")
    popup.geometry("1000x500")
    popup.configure(bg="cadetblue")  # Fundal pentru fereastra pop-up

    # Confirmation message
    label = tk.Label(popup, text=f"Produsul '{product_name}' a fost adăugat în coș!", font=("Arial", 12, "bold"), pady=10, bg="cadetblue", fg="white")
    label.pack()

    # Select 3 random recommended products
    recommended = random.sample(products, min(3, len(products)))

    # Stil pentru ttk.LabelFrame
    style = ttk.Style()
    style.configure("Custom.TFrame", background="cadetblue")

    # Frame pentru produsele recomandate
    rec_frame = ttk.Frame(popup, style="Custom.TFrame")  # Folosim un Frame simplu, fără LabelFrame
    rec_frame.pack(fill="both", padx=10, pady=5, expand=True)

    # Text pentru recomandări
    recommendation_label = tk.Label(rec_frame, text="S-ar putea să-ți placă și:", font=("Arial", 12, "bold"), bg="cadetblue", fg="white")
    recommendation_label.pack(fill='x', pady=5, anchor='center')  # Centrat și fără chenar

    for product in recommended:
        product_frame = ttk.Frame(rec_frame, style="Custom.TFrame")  # Fundal
        product_frame.pack(fill='x', pady=5)

        img_path = os.path.join("app/images", os.path.basename(product["imagine"]))
        img = load_image(img_path, 100, 100)

        img_label = tk.Label(product_frame, image=img, bg="cadetblue")
        img_label.image = img
        img_label.pack(side='left', padx=10)

        if category == "Alimente":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\nIngrediente: {product['ingrediente']}\nCantitate: {product['cantitate']}\n{product['descriere']}"
        elif category == "Fashion":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\nCuloare: {product['culoare']}\n{product['descriere']}"    
        elif category == "Electronice":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\n{product['descriere']}"    
        else:
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\n{product['descriere']}"

        text_label = tk.Label(product_frame, text=text, justify='left', anchor='w', bg="cadetblue", fg="white")
        text_label.pack(side='left', padx=10)

        cart_icon = load_image("app/images/cos-de-cumparaturi.png", 30, 30)
        if cart_icon:
            cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["nume_produs"]: add_to_cart(p, category, products), bg="cadetblue", borderwidth=0)
            cart_button.image = cart_icon
            cart_button.pack(side='right', padx=10)

    close_button = ttk.Button(popup, text="OK", command=popup.destroy)
    close_button.pack(pady=10)


def display_products(parent, category, products):
    # Folosește doar un Frame simplu pentru a înlocui LabelFrame
    frame = ttk.Frame(parent, padding=10, style="Custom.TFrame")  # Folosește Frame în loc de LabelFrame
    frame.pack(padx=10, pady=10, fill='x')

    # Centrarea numelui categoriei
    label = tk.Label(frame, text=category, font=("Arial", 12, "bold"), bg="cadetblue", fg="white")
    label.pack(fill='x', pady=5, anchor='center')  # Aici am adăugat `anchor='center'` pentru a centra textul

    for product in products:
        product_frame = ttk.Frame(frame, style="Custom.TFrame")  # Folosește stilul "Custom.TFrame" fără eticheta default
        product_frame.pack(fill='x', pady=5)

        image_path = os.path.join("app/images", os.path.basename(product["imagine"]))
        image = load_image(image_path, 150, 150)

        img_label = tk.Label(product_frame, image=image, bg="cadetblue")  # Fundal la imagine
        img_label.image = image
        img_label.pack(side='left', padx=10)

        if category == "Alimente":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\nIngrediente: {product['ingrediente']}\nCantitate: {product['cantitate']}\n{product['descriere']}"
        elif category == "Fashion":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\nCuloare: {product['culoare']}\n{product['descriere']}"    
        elif category == "Electronice":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\n{product['descriere']}"    
        else:
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\n{product['descriere']}"    

        text_label = tk.Label(product_frame, text=text, justify='left', anchor='w', bg="cadetblue", fg="white")  # Fundal la text
        text_label.pack(side='left', padx=10)

        # Iconiță coș de cumpărături
        cart_icon = load_image("app/images/cos-de-cumparaturi.png", 30, 30)  # Iconița de coș
        if cart_icon:
            cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["nume_produs"]: add_to_cart(p, category, products), bg="cadetblue", borderwidth=0)
            cart_button.image = cart_icon
            cart_button.pack(side='right', padx=10)


def on_mouse_wheel(event, canvas):
	if event.delta > 0:
		canvas.yview_scroll(-1, "units")
	else:
		canvas.yview_scroll(1, "units")

root = tk.Tk()
root.title("Catalog Produse")
root.geometry("1000x700")
root.configure(bg="cadetblue")

# 🔹 Define style for frame and add layout
style = ttk.Style()
style.configure("Custom.TFrame", background="cadetblue")
#style.configure("Custom.TLabelFrame", 
#                background="cadetblue",  # Fundalul pentru LabelFrame
#                foreground="white", 
#                font=("Arial", 12, "bold"))

#style.configure("Custom.TLabelFrame.label", 
#                background="cadetblue",  # Fundal cadetblue pentru text
#                foreground="white", 
#                font=("Arial", 12, "bold"))

#style.layout("Custom.TLabelFrame",
#             [("TLabelFrame.label", {"sticky": "w"}),
#              ("TLabelFrame.frame", {"sticky": "nsew"})])

#style.configure("Custom.TLabel", background="cadetblue", foreground="white")

# 🔹 Canvas pentru scroll și fundal
canvas = tk.Canvas(root, bg="cadetblue")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)

scroll_frame = ttk.Frame(canvas, style="Custom.TFrame")  # Aplicăm stilul
scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 🔹 Aplică stilul și în display_products
for category, products in data["categories"][0].items():
    display_products(scroll_frame, category.capitalize(), products)

root.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas))
root.mainloop()
