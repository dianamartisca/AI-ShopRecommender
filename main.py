import os
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

with open('app/resources/data.json', 'r', encoding='utf-8') as f:
	data = json.load(f)


def load_image(file_path):
	try:
		if not os.path.exists(file_path):
			print(f"Eroare: Fișierul {file_path} nu există.")
			return None

		image = Image.open(file_path)
		image = image.resize((150, 150), Image.LANCZOS)
		return ImageTk.PhotoImage(image)
	except Exception as e:
		print(f"Eroare la încărcarea imaginii: {e}")
		return None


def display_products(parent, category, products):
	frame = ttk.LabelFrame(parent, text=category, padding=10)
	frame.pack(padx=10, pady=10, fill='x')

	for product in products:
		product_frame = ttk.Frame(frame)
		product_frame.pack(fill='x', pady=5)

		image_path = os.path.join("app/images", os.path.basename(product["imagine"]))
		image = load_image(image_path)

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


def on_mouse_wheel(event, canvas):
	if event.delta > 0:
		canvas.yview_scroll(-1, "units")
	else:
		canvas.yview_scroll(1, "units")


root = tk.Tk()
root.title("Catalog Produse")
root.geometry("600x700")

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
