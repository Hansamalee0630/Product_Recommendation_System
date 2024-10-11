import sqlite3

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create a table for products
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    image_url TEXT
)
''')

# Insert product names into the database
products = [
    ('Nicole by OPI Nail Lacquer, Next Stop the Bikini Zone A59, .5 fl oz', 'opi', 'https://i5.walmartimages.com/asr/a3436bdc-e2e5-4c0c-b55c-0b2cbfbd7757_1.dfbc7c5baecd7674a3dfb60c84daf4b7.jpeg | https://i5.walmartimages.com/asr/c2a0f417-6ff8-4897-90d1-245c95120968_1.fbe74583b49fae6e244072d37ecdfae7.jpeg | https://i5.walmartimages.com/asr/2b9ad826-a70f-4840-bd44-13aa1470333f_1.872ac5b64b61e2cc492e5cf7e748f0fb.jpeg | https://i5.walmartimages.com/asr/9ff61eaf-7d12-4e46-b952-8a621119f308_1.1d4cecd3bcac85150a68e70d3325c307.jpeg | https://i5.walmartimages.com/asr/da0b9c90-5ef0-468d-931a-2bb9fdf3793d_1.a609ee51799b22f581278fcdb3feb3f5.jpeg | https://i5.walmartimages.com/asr/75dbca18-fec4-4c55-abd1-04a576b35c11_1.80f4e1d7e02cb992f129610a507ae83e.jpeg'),
    ('ReNew Life CleanseMore, Veggie Caps, 60 ea', 'renew, life', 'https://i5.walmartimages.com/asr/9f707fe4-9ee3-4dc5-b230-0005d2ba6f29_1.3b8ea51118f73b8528bbc6b808dd4ba4.jpeg | https://i5.walmartimages.com/asr/3fdd4912-70c4-4d75-bb00-72e390c9d6ac_1.db8927d28da7bb33697d9eff3b206fb8.jpeg'),
    ('Candle Warmers Etc. Rustic Brown Hurricane Candle Warmer Lantern', 'candle, warmers, etc', 'https://i5.walmartimages.com/asr/54376245-b5c1-4d6a-9972-bc41a2a825ea_1.f46b3671e8d222adc37867e197457837.png'),
    ('Recovery Complex Anti-Frizz Shine Serum by Bain de Terre for Unisex, 4.2 oz', 'bain, de, terre', 'https://i5.walmartimages.com/asr/fcdb4d2e-3727-4bc4-bb2a-63c585c236b0_1.4c8c7111e5dde79bad7e54b6f71a8781.jpeg | https://i5.walmartimages.com/asr/1e8c5630-bd1b-42bf-b29b-328734e30ea1_1.1c9ebfea6bdb2db875f2dad0f9e29b76.jpeg | https://i5.walmartimages.com/asr/a0be5e6f-2b7d-4949-a146-c6d36fc1e3bc_1.f3060628a171205ba3854294a3a300fc.jpeg | https://i5.walmartimages.com/asr/681df146-a265-4f3e-87ed-face6fffcd8a_1.845d323e06801631b2ecaf4a5a3b21d2.jpeg'),
    ('Vega Chlorella Dietary Supplement Powder 5.3 oz. Bottle', 'vega', 'https://i5.walmartimages.com/asr/e8ddd649-4959-4454-9798-cc185525baa6_1.c98f8adaf041556d63baadedf00316a9.jpeg | https://i5.walmartimages.com/asr/530a22d0-2e8b-4adc-99ef-7ffe4991422e_1.d6323950626acdfcc07e10a688c65ef5.jpeg | https://i5.walmartimages.com/asr/bf1b0107-e155-4186-899e-7657a21426dd_1.d6b02a5cb8f9664a850ff6be3293a18a.jpeg'),
    
    ('Alaffia Body Lotion, Vanilla, 32 Oz', 'alaffia', 'https://i5.walmartimages.com/asr/2988c323-cb6f-4a45-9bd7-9029d981630c_1.d65b6410f1b5a72233cdab07e25e153b.jpeg | https://i5.walmartimages.com/asr/c773f069-a99d-4d06-a4ff-d4c839063929_1.3a72dc9092da4efd57530dc86a077c6d.jpeg'),
]

# Fetch all products
cursor.execute('SELECT * FROM products')
all_products = cursor.fetchall()

# Print the products
for product in all_products:
    print(product)

# Insert products into the database
cursor.executemany('INSERT INTO products (name, brand, image_url) VALUES (?, ?, ?)', products)
conn.commit()
conn.close()
