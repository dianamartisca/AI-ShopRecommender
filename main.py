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
        if image.mode == "RGBA":
            image = image.resize((x, y), Image.LANCZOS)
        else:
            image = image.convert("RGBA").resize((x, y), Image.LANCZOS)

        return ImageTk.PhotoImage(image)
    
    except Exception as e:
        print(f"Eroare la încărcarea imaginii: {e}")
        return None

def add_to_cart(product_name, category, products):
    """ Display a pop-up when a product is added to the cart, along with recommended products. """
    popup = tk.Toplevel()
    popup.title("Added to Cart")
    popup.geometry("1000x700")
    popup.configure(bg="#2F4F4F")  # Fundal pentru fereastra pop-up

    # Confirmation message
    label = tk.Label(popup, text=f"Produsul '{product_name}' a fost adăugat în coș!", font=("Georgia", 15, "bold"), pady=10, bg="#2F4F4F", fg="white")
    label.pack()

    # Select 3 random recommended products
    recommended = random.sample(products, min(3, len(products)))

    style = ttk.Style()
    style.configure("Custom.TFrame", background="#2F4F4F")

    # Frame pentru produsele recomandate
    rec_frame = ttk.Frame(popup, style="Custom.TFrame")  # Folosim un Frame simplu, fără LabelFrame
    rec_frame.pack(fill="both", padx=10, pady=5, expand=True)

    # Text pentru recomandări
    recommendation_label = tk.Label(rec_frame, text="S-ar putea să-ți placă și:", font=("Georgia", 13, "bold"), bg="#2F4F4F", fg="white", anchor='w')  # Aliniat la stânga
    recommendation_label.pack(fill='x', pady=5)  


    for product in recommended:
        product_frame = ttk.Frame(rec_frame, style="Custom.TFrame")  # Fundal
        product_frame.pack(fill='x', pady=5)

        img_path = os.path.join("app/images", os.path.basename(product["imagine"]))
        img = load_image(img_path, 150, 150)

        img_label = tk.Label(product_frame, image=img, bg="#2F4F4F")
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

        text_label = tk.Label(product_frame, text=text, justify='left', anchor='w', bg="#2F4F4F", fg="white", font=("Georgia", 10))
        text_label.pack(side='left', padx=10)

        cart_icon = load_image("app/images/cos-de-cumparaturi.png", 40, 40)
        if cart_icon:
            cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["nume_produs"]: add_to_cart(p, category, products), bg="#2F4F4F", borderwidth=0)
            cart_button.image = cart_icon
            cart_button.pack(side='right', padx=10)

    close_button = ttk.Button(popup, text="OK", command=popup.destroy)
    close_button.pack(pady=10)


def display_products(parent, category, products):
    frame = ttk.Frame(parent, padding=10, style="Custom.TFrame")  
    frame.pack(padx=10, pady=10, fill='x')

    # Textul pentru categoria respectivă, aliniat la stânga
    label = tk.Label(frame, text=category, font=("Georgia", 15, "bold"), bg="#2F4F4F", fg="white", anchor='w')
    label.pack(fill='x', pady=5)  # Aliniat la stânga (anchor='w')


    for product in products:
        product_frame = ttk.Frame(frame, style="Custom.TFrame")  
        product_frame.pack(fill='x', pady=5)

        image_path = os.path.join("app/images", os.path.basename(product["imagine"]))
        image = load_image(image_path, 150, 150)

        img_label = tk.Label(product_frame, image=image, bg="#2F4F4F")  # Fundal la imagine
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

        text_label = tk.Label(product_frame, text=text, justify='left', anchor='w', bg="#2F4F4F", fg="white", font=("Georgia", 10))  # Fundal la text
        text_label.pack(side='left', padx=10)

        # Iconiță coș de cumpărături
        cart_icon = load_image("app/images/cos-de-cumparaturi.png", 40, 40)  # Iconița de coș
        if cart_icon:
            cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["nume_produs"]: add_to_cart(p, category, products), bg="#2F4F4F", borderwidth=0)
            cart_button.image = cart_icon
            cart_button.pack(side='right', padx=10)


def on_mouse_wheel(event, canvas):
	if event.delta > 0:
		canvas.yview_scroll(-1, "units")
	else:
		canvas.yview_scroll(1, "units")

root = tk.Tk()
root.title("Catalog Produse")
root.geometry("1250x700")
root.configure(bg="#2F4F4F")

# 🔹 Define style for frame and add layout
style = ttk.Style()
style.configure("Custom.TFrame", background="#2F4F4F")
#style.configure("Custom.TLabelFrame", 
#                background="#2F4F4F",  # Fundalul pentru LabelFrame
#                foreground="white", 
#                font=("Georgia", 12, "bold"))

#style.configure("Custom.TLabelFrame.label", 
#                background="#2F4F4F",  # Fundal #2F4F4F pentru text
#                foreground="white", 
#                font=("Georgia", 12, "bold"))

#style.layout("Custom.TLabelFrame",
#             [("TLabelFrame.label", {"sticky": "w"}),
#              ("TLabelFrame.frame", {"sticky": "nsew"})])

#style.configure("Custom.TLabel", background="#2F4F4F", foreground="white")

# 🔹 Canvas pentru scroll și fundal
canvas = tk.Canvas(root, bg="#2F4F4F")
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
