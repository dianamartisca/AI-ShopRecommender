import os
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

with open('app/resources/data.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

all_products = []
for category_products in data["categories"][0].values():
    all_products.extend(category_products)


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

def add_to_cart(product_name):
    """ Display a pop-up when a product is added to the cart, along with recommended products. """
    popup = tk.Toplevel()
    popup.title("Added to Cart")
    popup.geometry("1000x500")

    # Confirmation message
    label = tk.Label(popup, text=f"Produsul '{product_name}' a fost adăugat în coș!", font=("Arial", 12), pady=10)
    label.pack()

    # Select 3 random recommended products
    recommended = random.sample(all_products, min(3, len(all_products)))

    # Frame for recommended products
    rec_frame = ttk.LabelFrame(popup, text="S-ar putea să-ți placă și:", padding=10)
    rec_frame.pack(fill="both", padx=10, pady=5, expand=True)

    for product in recommended:
        product_frame = ttk.Frame(rec_frame)
        product_frame.pack(fill='x', pady=5)

        img_path = os.path.join("app/images", os.path.basename(product["imagine"]))
        img = load_image(img_path, 100, 100)  # Smaller image for recommendations

        img_label = tk.Label(product_frame, image=img)
        img_label.image = img
        img_label.pack(side='left', padx=10)

        # Generate detailed text like in display_products
        text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\n{product['descriere']}"
        if 'ingrediente' in product:
            text += f"\nIngrediente: {product['ingrediente']}"
        if 'cantitate' in product:
            text += f"\nCantitate: {product['cantitate']}"
        if 'culoare' in product:
            text += f"\nCuloare: {product['culoare']}"

        text_label = tk.Label(product_frame, text=text, justify='left', anchor='w')
        text_label.pack(side='left', padx=10)

        cart_icon = load_image("app/images/cos-de-cumparaturi.png", 30, 30)  # Smaller cart icon
        if cart_icon:
            cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["nume_produs"]: add_to_cart(p))
            cart_button.image = cart_icon
            cart_button.pack(side='right', padx=10)

    close_button = ttk.Button(popup, text="OK", command=popup.destroy)
    close_button.pack(pady=10)


def display_products(parent, category, products):
	frame = ttk.LabelFrame(parent, text=category, padding=10)
	frame.pack(padx=10, pady=10, fill='x')

	for product in products:
		product_frame = ttk.Frame(frame)
		product_frame.pack(fill='x', pady=5)

		image_path = os.path.join("app/images", os.path.basename(product["imagine"]))
		image = load_image(image_path, 150, 150)

		# image = load_image(product["imagine"])
		img_label = tk.Label(product_frame, image=image)
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
		text_label = tk.Label(product_frame, text=text, justify='left', anchor='w')
		text_label.pack(side='left', padx=10)

		# Iconiță coș de cumpărături
		cart_icon = load_image("app/images/cos-de-cumparaturi.png", 30, 30)  # Iconița de coș
		if cart_icon:
			cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["nume_produs"]: add_to_cart(p))
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

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_frame = ttk.Frame(canvas)
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

for category, products in data["categories"][0].items():
	display_products(scroll_frame, category.capitalize(), products)

root.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas))

root.mainloop()
