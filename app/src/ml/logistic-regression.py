import json
import numpy as np
import re
import os
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.preprocessing.text import Tokenizer


#citirea datelor
def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
     
data = read_data('app/resources/data.json')


#preprocesarea datelor
all_products = []

for category, products in data["categories"][0].items():
    if category == "alimente":
        for product in products:
            one_product = f"{category} {product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product['ingrediente']} {product['cantitate']} {product.get('descriere', '')}"
            all_products.append(one_product)
    elif category == "fashion":
        for product in products:
            one_product = f"{category} {product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product['culoare']} {product.get('descriere', '')}"
            all_products.append(one_product)
    elif category == "electronice":
        for product in products:
            one_product = f"{category} {product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product.get('descriere', '')}"
            all_products.append(one_product)
    else:
        for product in products:
            one_product = f"{category} {product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product.get('descriere', '')}"
            all_products.append(one_product)

for index in range(len(all_products)):
    all_products[index] = re.sub(r'[^\w\s]','',all_products[index])
#all_products = ["1 " + produs for produs in all_products]
#print(all_products)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_products)
tokenized_sequences = tokenizer.texts_to_sequences(all_products)
#print(tokenized_sequences)

max_input_length = max(len(seq) for seq in tokenized_sequences)
#print(f'Combined max sequence length is {max_input_length}')

padded_sequences = preprocessing.sequence.pad_sequences(tokenized_sequences, maxlen=max_input_length, padding='post')
input_data = np.array(padded_sequences)
bias_column = np.ones((input_data.shape[0], 1))  # Column of ones
input_data = np.hstack((bias_column, input_data))
print(f'Input data shape -> {input_data.shape}')
#print(input_data)

input_word_dict = tokenizer.word_index
num_input_tokens = len( input_word_dict )+1
print('Number of input tokens = {}'.format( num_input_tokens))
#print(input_word_dict)


#prepararea datelor
p = np.random.permutation(len(input_data))
input_data = input_data[p]

train_size = int(0.6 * len(input_data))
val_size = int(0.2 * len(input_data))
test_size = len(input_data) - train_size - val_size

train_input = input_data[:train_size]
validation_input = input_data[train_size:train_size + val_size]
test_input = input_data[train_size + val_size:]

print('Train input shape:', train_input.shape)
print('Validation input shape:', validation_input.shape)
print('Test input shape:', test_input.shape)


#functia sigmoid
def sigm(x):
    return 1/(1+np.exp(-x))

def perceptron(x, w0, w1):
    x = x * w1 + w0
    return sigm(x)

