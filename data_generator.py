import json
import random
import os
from faker import Faker
from config import USERS_FILENAME, PRODUCTS_FILENAME, TRANSACTIONS_FILENAME

class DataGenerator:
    def __init__(self):
        pass
    
    def __save_file(self, path, data):
        if not os.path.exists(path):   
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
    
    def generate_users(self):
        fake = Faker()

        data = []

        for i in range(0, 20):
            data.append({
                "user_id": i,
                "name": fake.name(),
                "country": fake.country()
            })

        self.__save_file(USERS_FILENAME, data)
        
                
    def generate_products(self):
        data = []

        categories = ["Laptops", "Smartphones", "Cameras", "Printers", "Tablets"]
        prices = [1899.99, 500.55, 674, 990.10, 679.98, None]

        for i in range(0, 20):
            data.append({
                "product_id": str(i),
                "category": categories[random.randint(0,4)],
                "price": prices[random.randint(0,5)]
            })
            
        self.__save_file(PRODUCTS_FILENAME, data)         
                
    def generate_transactions(self):
        data = []
        statuses = ["COMPLETED", "CANCELLED", "RETURNED"]

        for i in range(0, 30):
            items = [{"product_id": random.randint(0, 19), "quantity": random.randint(1, 15)} for _ in range(0, random.randint(0, 5))]
            timestamp = f"{random.randint(2023, 2025)}-{random.randint(1,12):02d}-{random.randint(1,31):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
            
            if i % 10 == 0:
                timestamp = f"{random.randint(2023, 2025)}-{random.randint(1,12):02d}-{random.randint(1,31):02d}{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

            
            data.append({
                "transaction_id": str(i),
                "user_id": random.randint(0, 19),
                "timestamp": timestamp,
                "items": items,
                "status": statuses[random.randint(0,2)]
            })
        
        self.__save_file(TRANSACTIONS_FILENAME, data)           