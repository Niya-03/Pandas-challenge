import json
import random
import os
from config import USERS_FILEPATH, PRODUCTS_FILEPATH, TRANSACTIONS_FILEPATH
from typing import List, Dict

class DataGenerator:
    def __init__(self):
        pass

    def __save_file(self, path: str, data: List[Dict]) -> None:
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(data, f, indent=4)

    def __generate_users(self) -> bool:
        try:
            data = []
            first_names = ["Angela", "Petar", "Anya", "John", "Ivan", "Gabriela"]
            last_names = ["Jones", "Peterson", "Andrews", "Doe", "Karamazov", "Mendoza"]

            countries = ["Bulgaria", "Spain", "Ireland", "USA", "UK"]

            for i in range(0, 20):
                data.append(
                    {
                        "user_id": i,
                        "name": f"{first_names[random.randint(0,5)]} {last_names[random.randint(0,5)]}",
                        "country": countries[random.randint(0, 4)],
                    }
                )

            self.__save_file(USERS_FILEPATH, data)

            return True

        except Exception as e:
            print(f"Error while generating users: {e}")
            return False

    def __generate_products(self) -> bool:
        try:
            data = []

            categories = ["Laptops", "Smartphones", "Cameras", "Printers", "Tablets"]
            prices = [1899.99, 500.55, 674, 990.10, 679.98, None]

            for i in range(0, 20):
                data.append(
                    {
                        "product_id": str(i),
                        "category": categories[random.randint(0, 4)],
                        "price": prices[random.randint(0, 5)],
                    }
                )

            self.__save_file(PRODUCTS_FILEPATH, data)

            return True

        except Exception as e:
            print(f"Error while generating products: {e}")
            return False

    def __generate_transactions(self) -> bool:
        try:
            data = []
            statuses = ["COMPLETED", "CANCELLED", "RETURNED"]

            for i in range(0, 30):
                items = [
                    {
                        "product_id": random.randint(0, 19),
                        "quantity": random.randint(1, 15),
                    }
                    for _ in range(0, random.randint(0, 5))
                ]
                timestamp = f"{random.randint(2023, 2025)}-{random.randint(1,12):02d}-{random.randint(1,31):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

                if i % 10 == 0:
                    timestamp = f"{random.randint(2023, 2025)}-{random.randint(1,12):02d}-{random.randint(1,31):02d}{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

                data.append(
                    {
                        "transaction_id": str(i),
                        "user_id": random.randint(0, 19),
                        "timestamp": timestamp,
                        "items": items,
                        "status": statuses[random.randint(0, 2)],
                    }
                )

            self.__save_file(TRANSACTIONS_FILEPATH, data)

            return True

        except Exception as e:
            print(f"Error while generating transactions: {e}")
            return False

    def generate_mock_data(self) -> bool:
        if not self.__generate_users():
            return False

        if not self.__generate_products():
            return False

        if not self.__generate_transactions():
            return False

        return True
