import json
import numpy as np
import re
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


#citirea datelor
def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


#preprocesarea datelor
def extract_data(data):
    all_products = []
    categories = []

    for category, products in data["categories"][0].items():
        if category == "alimente":
            for product in products:
                one_product = f"{product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product['ingrediente']} {product['cantitate']} {product.get('descriere', '')}"
                all_products.append(one_product)
                categories.append(category)
        elif category == "fashion":
            for product in products:
                one_product = f"{product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product['culoare']} {product.get('descriere', '')}"
                all_products.append(one_product)
                categories.append(category)
        elif category == "electronice":
            for product in products:
                one_product = f"{product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product.get('descriere', '')}"
                all_products.append(one_product)
                categories.append(category)
        else:
            for product in products:
                one_product = f"{product['nume_produs']} {product['nume_producator']} {product['pret']} RON {product['rating']} rating {product.get('descriere', '')}"
                all_products.append(one_product)
                categories.append(category)
    
    return all_products, categories

def preprocess_input(all_products):
    for index in range(len(all_products)):
        all_products[index] = re.sub(r'[^\w\s]','',all_products[index])

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
    #print(f'Input data shape -> {input_data.shape}')
    input_word_dict = tokenizer.word_index
    #num_input_tokens = len( input_word_dict )+1
    #print('Number of input tokens = {}'.format( num_input_tokens))
    #print(input_word_dict)

    return input_data, max_input_length, input_word_dict

def preprocess_output(categories):
    unique_entries = list(set(categories))
    output_word_dict = {entry: index for index, entry in enumerate(unique_entries)}
    tokenized_categories = [[output_word_dict[entry]] for entry in categories]
    #max_output_length = max(len(token_seq) for token_seq in tokenized_categories)
    #print('Output max length is {}'.format(max_output_length))
    output_data = np.array(tokenized_categories)
    #print('Output data shape -> {}'.format(output_data.shape))
    #print(output_data)
    num_output_tokens = len(output_word_dict) 
    #print('Number of output tokens = {}'.format(num_output_tokens))
    #print(output_word_dict)

    return output_data, output_word_dict, num_output_tokens


#separarea datelor
def split_data(input_data, output_data):
    p = np.random.permutation(len(input_data))
    input_data = input_data[p]

    train_size = int(0.8 * len(input_data))

    train_input = input_data[:train_size]
    test_input = input_data[train_size:]
    #print('Train input shape:', train_input.shape)
    #print('Test input shape:', test_input.shape)

    train_output = output_data[:train_size]
    test_output = output_data[train_size:]
    #print('Train output shape:', train_output.shape)
    #print('Test output shape:', test_output.shape)

    return train_input, test_input, train_output, test_output


#functia sigmoid
def sigm(x):
    x_clipped = np.clip(x, -500, 500)
    return 1/(1+np.exp(-x_clipped))


#functia softmax
def softmax(z):
    exp_z = np.exp(z - np.max(z))  
    return exp_z / np.sum(exp_z)


#functia gradient_descent
def gradient_descent(X, y, theta, learning_rate, iterations):

    # X: matricea caracteristicilor (m x n)
    # y: vectorul țintă (m x num_classes) cu valori 0 sau 1
    # theta: vectorul inițial al parametrilor (n x 1)

    m = len(y)  

    for _ in range(iterations):
        predictions = sigm(X @ theta)  
        errors = predictions - y  
        gradient = (1/m) * (X.T @ errors)  
        theta -= learning_rate * gradient  

    return theta  


#functia train
def train(X, y, num_classes, learning_rate=0.01, iterations=1000):
    m, n = X.shape  
    all_theta = np.zeros((n, num_classes))  

    for c in range(num_classes):
        y_c = (y == c).astype(int)  
        theta = np.random.randn(n, 1)  
        all_theta[:, c] = gradient_descent(X, y_c, theta, learning_rate, iterations).flatten()

    return all_theta  

def train_model():
    data = read_data('app/resources/data.json')
    all_products, categories = extract_data(data)
    input_data, max_input_length, input_word_dict = preprocess_input(all_products)
    output_data, output_word_dict, num_output_tokens = preprocess_output(categories)
    train_input, test_input, train_output, test_output = split_data(input_data, output_data)
    all_theta = train(train_input, train_output, num_output_tokens)
    #print("Shape of all_theta:", all_theta.shape)

    return all_theta, input_word_dict, output_word_dict, max_input_length

all_theta, input_word_dict, output_word_dict, max_input_length = train_model()

#functia predict
def predict_multiclass(X):
    z = X @ all_theta  
    probabilities = softmax(z) 
    return np.argmax(probabilities, axis=1).item()

def predict(product):
    product = re.sub(r'[^\w\s]','',product)
    words = product.split()
    words = [word.lower() for word in words]
    tokenized_text = [[input_word_dict[entry]] for entry in words]
    tokenized_text = pad_sequences([tokenized_text], maxlen=max_input_length, padding='post')   
    X = tokenized_text.flatten().reshape(1, max_input_length)
    X = np.hstack((np.ones((X.shape[0], 1)), X))
    #print(X.shape)
    #print(X)
    category_index = predict_multiclass(X)
    index_to_category = {index: category for category, index in output_word_dict.items()}
    category = index_to_category.get(category_index, "Unknown")
    #print(category)
    #print(category_index)
    return category