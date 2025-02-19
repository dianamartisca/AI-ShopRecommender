import os
import json
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import warnings
import tensorflow as tf
import numpy as np
from transformers import pipeline
from transformers.utils import logging
from app.src.ml.logistic_regression import predict
from sentence_transformers import SentenceTransformer, util

# Suppress all TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  
tf.get_logger().setLevel("ERROR")  

# Suppress all warnings from Python and Transformers
warnings.filterwarnings("ignore")
logging.set_verbosity_error()

with open('app/resources/data.json', 'r', encoding='utf-8') as f:
	data = json.load(f)
     
def extract_products(data):
    all_products = []

    for category, products in data["categories"][0].items():
        for product in products:
            product_id = product["id"]
            product_name = product["nume_produs"]

            details = f"{product['nume_producator']} {product['pret']} RON {product['rating']} rating"
        
            if category == "alimente":
                details += f" {product['ingrediente']} {product['cantitate']} {product.get('descriere', '')}"
            elif category == "fashion":
                details += f" {product['culoare']} {product.get('descriere', '')}"
            else: 
                details += f" {product.get('descriere', '')}"
        
            all_products.append({
                "id": product_id,
                "nume_produs": product_name,
                "rest": details.strip()
            })
    return all_products

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

def add_to_cart(product_id):
    """ Display a pop-up when a product is added to the cart, along with recommended products. """
    popup = tk.Toplevel()
    popup.title("Added to Cart")
    popup.geometry("1000x700")
    popup.configure(bg="#2F4F4F")  

    all_products = extract_products(data)
    for product in all_products:
        if product["id"] == product_id:
            product_name = product["nume_produs"]
            product_details = product["rest"]
            text = f"{product_name} {product_details}"
            break

    # Confirmation message
    label = tk.Label(popup, text=f"Produsul '{product_name}' a fost adăugat în coș!", font=("Georgia", 15, "bold"), pady=10, bg="#2F4F4F", fg="white")
    label.pack()

    # Select 3 random recommended products from the predicted category
    category = predict(text)
    categories = data["categories"][0] 
    products = categories[category]
    filtered_products = [p for p in products if p["id"] != product_id]
    recommended = random.sample(filtered_products, min(3, len(filtered_products)))

    style = ttk.Style()
    style.configure("Custom.TFrame", background="#2F4F4F")

    # Frame pentru produsele recomandate
    rec_frame = ttk.Frame(popup, style="Custom.TFrame")  
    rec_frame.pack(fill="both", padx=10, pady=5, expand=True)

    # Text pentru recomandări
    recommendation_label = tk.Label(rec_frame, text="S-ar putea să-ți placă și:", font=("Georgia", 13, "bold"), bg="#2F4F4F", fg="white", anchor='w')  # Aliniat la stânga
    recommendation_label.pack(fill='x', pady=5)  

    for product in recommended:
        product_frame = ttk.Frame(rec_frame, style="Custom.TFrame") 
        product_frame.pack(fill='x', pady=5)

        img_path = os.path.join("app/images", os.path.basename(product["imagine"]))
        img = load_image(img_path, 150, 150)

        img_label = tk.Label(product_frame, image=img, bg="#2F4F4F")
        img_label.image = img
        img_label.pack(side='left', padx=10)

        if category == "alimente":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\nIngrediente: {product['ingrediente']}\nCantitate: {product['cantitate']}\n{product['descriere']}"
        elif category == "fashion":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\nCuloare: {product['culoare']}\n{product['descriere']}"    
        elif category == "electronice":
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\n{product['descriere']}"    
        else:
            text = f"{product['nume_produs']}\n{product['nume_producator']}\n{product['pret']} RON\nRating: {product['rating']}\n{product['descriere']}"

        text_label = tk.Label(product_frame, text=text, justify='left', anchor='w', bg="#2F4F4F", fg="white", font=("Georgia", 10))
        text_label.pack(side='left', padx=10)

        cart_icon = load_image("app/images/cos-de-cumparaturi.png", 40, 40)
        if cart_icon:
            cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["id"]: add_to_cart(p), bg="#2F4F4F", borderwidth=0)
            cart_button.image = cart_icon
            cart_button.pack(side='right', padx=10)

    close_button = ttk.Button(popup, text="OK", command=popup.destroy)
    close_button.pack(pady=10)

def display_products(parent, category, products):
    frame = ttk.Frame(parent, padding=10, style="Custom.TFrame")  
    frame.pack(padx=10, pady=10, fill='x')

    # Textul pentru categoria respectivă, aliniat la stânga
    label = tk.Label(frame, text=category, font=("Georgia", 15, "bold"), bg="#2F4F4F", fg="white", anchor='w')
    label.pack(fill='x', pady=5)  

    for product in products:
        product_frame = ttk.Frame(frame, style="Custom.TFrame")  
        product_frame.pack(fill='x', pady=5)

        image_path = os.path.join("app/images", os.path.basename(product["imagine"]))
        image = load_image(image_path, 150, 150)

        img_label = tk.Label(product_frame, image=image, bg="#2F4F4F")  
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

        text_label = tk.Label(product_frame, text=text, justify='left', anchor='w', bg="#2F4F4F", fg="white", font=("Georgia", 10))  
        text_label.pack(side='left', padx=10)

        # Iconiță coș de cumpărături
        cart_icon = load_image("app/images/cos-de-cumparaturi.png", 40, 40)  
        if cart_icon:
            cart_button = tk.Button(product_frame, image=cart_icon, command=lambda p=product["id"]: add_to_cart(p), bg="#2F4F4F", borderwidth=0)
            cart_button.image = cart_icon
            cart_button.pack(side='right', padx=10)

def on_mouse_wheel(event, canvas):
	if event.delta > 0:
		canvas.yview_scroll(-1, "units")
	else:
		canvas.yview_scroll(1, "units")

def chatbot(products):
    print("Eu sunt asistentul tău virtual. Cu ce te pot ajuta?")
    while True:
        question = input("Întrebare: ")
        qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
        result = qa_pipeline(question=question, context=products)
        print("Răspuns:", result["answer"]) 

'''def chatbot(products):
    # Load a pre-trained Sentence Transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Convert all product descriptions to embeddings
    product_embeddings = model.encode(products, convert_to_tensor=True)

    print("Eu sunt asistentul tău virtual. Cu ce te pot ajuta?")
    while True:
        # User's question
        question = input("Întrebare: ")
        if question.lower() == "exit":
            break
        # Embed the question
        query_embedding = model.encode(question, convert_to_tensor=True)
        # Compute cosine similarities
        similarities = util.pytorch_cos_sim(query_embedding, product_embeddings)[0]  # [0] because it's a 2D tensor
        best_match_idx = int(similarities.argmax())  # Get the index of the highest similarity
        # Print the most relevant product
        print(f"Răspuns: {products[best_match_idx]}")'''

def chatbot_data(data):
    all_products = []
    for category, products in data["categories"][0].items():
        if category == "alimente":
            for product in products:
                one_product = f"Produsul din categoria {category} cu numele {product['nume_produs']} este produs de {product['nume_producator']}, are prețul {product['pret']} RON, ratingul {product['rating']}, ingredientele {product['ingrediente']}, cantitatea {product['cantitate']} și este {product['descriere']}."
                all_products.append(one_product)
        elif category == "fashion":
            for product in products:
                one_product = f"Produsul din categoria {category} cu numele {product['nume_produs']} este produs de {product['nume_producator']}, are prețul {product['pret']} RON, ratingul {product['rating']}, culoarea {product['culoare']} și este {product['descriere']}."
                all_products.append(one_product)
        else:
            for product in products:
                one_product = f"Produsul din categoria {category} cu numele {product['nume_produs']} este produs de {product['nume_producator']}, are prețul {product['pret']} RON, ratingul {product['rating']} și este {product['descriere']}."
                all_products.append(one_product)
    return "\n".join(all_products)

products_chatbot = chatbot_data(data)
chatbot_thread = threading.Thread(target=chatbot, args=(products_chatbot,), daemon=True)
chatbot_thread.start()

root = tk.Tk()
root.title("Catalog Produse")
root.geometry("1250x700")
root.configure(bg="#2F4F4F")

style = ttk.Style()
style.configure("Custom.TFrame", background="#2F4F4F")

# Canvas pentru scroll și fundal
canvas = tk.Canvas(root, bg="#2F4F4F")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)

scroll_frame = ttk.Frame(canvas, style="Custom.TFrame")  
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

# Aplică stilul și în display_products
for category, products in data["categories"][0].items():
    display_products(scroll_frame, category.capitalize(), products)

root.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas))
root.mainloop()