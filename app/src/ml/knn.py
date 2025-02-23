from sentence_transformers import SentenceTransformer, util
import json
import math

with open('app/resources/data.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

# Initialize the model
similarity_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def det_similarity_score(string1, string2):
    # Encode both strings into embeddings
    embeddings = similarity_model.encode([string1, string2], convert_to_tensor=True)
    # Calculate cosine similarity between the two embeddings
    cosine_similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    # Extract similarity score as a scalar
    similarity_score = cosine_similarity.item()

    return similarity_score

def extract_products(data):
    all_products = []

    for category, products in data["categories"][0].items():
        for product in products:
            id = product["id"]
            product_name = product["nume_produs"]
            man_name = product["nume_producator"]
            price = product["pret"]
            rating = product["rating"]
            details = product["descriere"]

            all_products.append({
                "id": id,
                "nume_produs": product_name,
                "nume_producator": man_name,
                "pret": price,
                "rating": rating,
                "descriere": details
            })
    return all_products

all_products = extract_products(data)

def get_product_info(product_id):
    for product in all_products:
        if product["id"] == product_id:
            return product
        
def predict_knn(product_id):
    top_three = [
        {"id": -1, "distance": 10000},
        {"id": -1, "distance": 10000},
        {"id": -1, "distance": 10000}
    ]
    neighbor = get_product_info(product_id)
    for product in all_products:
        if product["id"] == neighbor["id"]:
            continue
        x = det_similarity_score(neighbor["nume_produs"], product["nume_produs"])
        y = det_similarity_score(neighbor["nume_producator"], product["nume_producator"])
        z = neighbor["pret"] - product["pret"]
        w = neighbor["rating"] - product["rating"]
        v = det_similarity_score(neighbor["descriere"], product["descriere"])

        distance = math.sqrt(x**2 + y**2 + z**2 + w**2 + v**2)
        for i in range(3):
            if distance < top_three[i]["distance"]:
                top_three.insert(i, {"id": product["id"], "distance": distance})
                top_three.pop()  # Remove the last one to maintain only three
                break
    id_list = [item["id"] for item in top_three]
    return id_list

#print(all_products[33]["id"])
#print(predict_knn(all_products[33]["id"]))
