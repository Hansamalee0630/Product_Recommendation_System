from flask import Flask, request, render_template,jsonify 
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import os


app = Flask(__name__)

# load files===========================================================================================================
trending_products = pd.read_csv(r"product\\data\\trending_products.csv")
train_data = pd.read_csv(r"product\\data\\clean_data.csv")



# Recommendations functions============================================================================================
# Function to truncate product name
def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text


def content_based_recommendations(train_data, item_name, top_n=10):
    # Check if the item name exists in the training data
    if item_name not in train_data['Name'].values:
        print(f"Item '{item_name}' not found in the training data.")
        return pd.DataFrame()

    # Create a TF-IDF vectorizer for item descriptions
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Apply TF-IDF vectorization to item descriptions
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])

    # Calculate cosine similarity between items based on descriptions
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    # Find the index of the item
    item_index = train_data[train_data['Name'] == item_name].index[0]

    # Get the cosine similarity scores for the item
    similar_items = list(enumerate(cosine_similarities_content[item_index]))

    # Sort similar items by similarity score in descending order
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    # Get the top N most similar items (excluding the item itself)
    top_similar_items = similar_items[1:top_n+1]

    # Get the indices of the top similar items
    recommended_item_indices = [x[0] for x in top_similar_items]

    # Get the details of the top similar items
    recommended_items_details = train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]

    return recommended_items_details


# routes===============================================================================
# List of predefined image URLs
random_image_urls = [
    "static/img/img_1.png",
    "static/img/img_2.png",
    "static/img/img_3.png",
    "static/img/img_4.png",
    "static/img/img_5.png",
    "static/img/img_6.png",
    "static/img/img_7.png",
    "static/img/img_8.png",
]

# Function to fetch matching products from SQLite
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # Fetch matching product names from the database
    cursor.execute("SELECT name FROM products WHERE name LIKE ? LIMIT 10", (f'%{query}%',))
    results = cursor.fetchall()
    
    # Extract product names from results
    product_names = [result[0] for result in results]
    
    conn.close()
    return jsonify(product_names)

@app.route("/")
def index():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html',trending_products=trending_products.head(8),truncate = truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price = random.choice(price))

@app.route("/main")
def main():
    return render_template('main.html')

# routes
@app.route("/index")
def indexredirect():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(price))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    products = data.get('products', [])
    # Logic to add products to the cart
    return jsonify({'success': True, 'message': 'Products added to cart!'})

# Checkout route
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')



@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    message = None  # Initialize message
    content_based_rec = None  # Initialize as None, so it's always passed to the template
    
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = request.form.get('nbr')

        if not nbr or not prod:
            message = "Please provide both a product and a number of recommendations."
            return render_template('main.html', message=message, content_based_rec=content_based_rec)

        nbr = int(nbr)  # Convert 'nbr' to an integer
        
        # Call your recommendation function
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

        if content_based_rec.empty:
            message = "No recommendations available for this product."
            return render_template('main.html', message=message, content_based_rec=content_based_rec)

        # Generate random image URLs and prices for recommendations
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(content_based_rec))]
        prices = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]  # Example prices
        
        return render_template('main.html', 
                               content_based_rec=content_based_rec, 
                               truncate=truncate, 
                               random_product_image_urls=random_product_image_urls,
                               random_price=random.choice(prices))  # Pass required data
    else:
        # On GET request, pass an empty DataFrame or None
        return render_template('main.html', content_based_rec=content_based_rec, message=message)


if __name__=='__main__':
    app.run(debug=True)
