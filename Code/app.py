from flask import Flask, render_template, request
import pickle 
import numpy as np
import pandas as pd


target_products = pickle.load(open('target_products_dict.pkl', 'rb'))
dot_product = pickle.load(open('dot_product_df.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_products', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # index = target_products[user_input]
    index = list(target_products.keys())[list(target_products.values()).index(user_input.lower())]
    similar_items = sorted(list(enumerate(dot_product[index])), key=lambda x:x[1], reverse=True)[1:100]
    print(similar_items)
    
    data = {}
    comple_prod = []
    count = 0
    
    for i, j in similar_items :
        if j < 0.96 and count < 5 :
            count += 1
            prod = target_products[i]
            data[prod] = j
            comple_prod.append(prod)
    print(f"comple_prod = {comple_prod}")
    print(f'user_input = {user_input}')
    
    return render_template('products.html', comple_prod=comple_prod, user_input=user_input)

if __name__ == "__main__" :
    app.run(debug=True)