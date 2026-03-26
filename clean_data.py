#  **Phase 1: Data Ingestion & Cleaning**
# *   Write a Python module to safely load the JSON files.
# *   Using `pandas`, flatten (normalize) the nested `items` list in the transaction data so that each row in your DataFrame 
# represents a **single item** purchased within a transaction.
# *   Clean the data:
#     *   Log and drop any transactions where the `timestamp` cannot be parsed into a valid datetime object.
#     *   Handle cases where a product price is missing or null. (Document your assumption on how you chose to handle this).

import pandas as pd
import os
import json

def load_json(path):
    if not os.path.exists(path):
        print(f"Error! {path} doesn't exist!")
        return None
        
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as error:
        print("Error loading {path}: {error}")
        return None
    

    
