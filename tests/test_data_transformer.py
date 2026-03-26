import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.data_transformer import DataTransformer


def test_clean_products_df_removes_missing_prices():
    data = [
        {"product_id": "0", "category": "Cameras", "price": 679.98},
        {"product_id": "1", "category": "Smartphones", "price": None},
        {"product_id": "2", "category": "Tablets", "price": 500.55},
    ]

    data_transformer = DataTransformer()
    data_transformer.products_df = pd.DataFrame(data)
    data_transformer._DataTransformer__clean_products_df()

    cleaned_df = data_transformer.products_df

    assert cleaned_df["price"].isna().sum() == 0

    assert len(cleaned_df) == 2


def test_clean_transactions_df_removes_invalid_timestamps():
    data = [
        {
            "transaction_id": "0",
            "user_id": 11,
            "timestamp": "2025-03-1800:25:53",
            "items": [
                {"product_id": 8, "quantity": 7},
                {"product_id": 14, "quantity": 8},
            ],
            "status": "RETURNED",
        },
        {
            "transaction_id": "1",
            "user_id": 4,
            "timestamp": "2023-02-31T16:54:16",
            "items": [
                {"product_id": 14, "quantity": 8},
                {"product_id": 9, "quantity": 15},
                {"product_id": 17, "quantity": 3},
            ],
            "status": "COMPLETED",
        },
        {
            "transaction_id": "2",
            "user_id": 8,
            "timestamp": "2024-07-05T18:34:33",
            "items": [{"product_id": 18, "quantity": 8}],
            "status": "CANCELLED",
        },
    ]

    data_transformer = DataTransformer()
    data_transformer.transactions_df = pd.DataFrame(data)
    data_transformer._DataTransformer__clean_transactions_df()

    cleaned_df = data_transformer.transactions_df

    assert len(cleaned_df) == 1

    remaining_ids = set(cleaned_df["transaction_id"])
    assert remaining_ids == {"2"}


def test_clean_transactions_df_removes_empty_items():
    data = [
        {
            "transaction_id": "0",
            "user_id": 11,
            "timestamp": "2025-03-1800:25:53",
            "items": [],
            "status": "RETURNED",
        },
        {
            "transaction_id": "1",
            "user_id": 4,
            "timestamp": "2023-12-14T16:54:16",
            "items": [
                {"product_id": 14, "quantity": 8},
                {"product_id": 9, "quantity": 15},
                {"product_id": 17, "quantity": 3},
                {"product_id": 4, "quantity": 3},
            ],
            "status": "COMPLETED",
        },
        {
            "transaction_id": "2",
            "user_id": 8,
            "timestamp": "2024-07-05T18:34:33",
            "items": [],
            "status": "CANCELLED",
        },
    ]

    data_transformer = DataTransformer()
    data_transformer.transactions_df = pd.DataFrame(data)
    data_transformer._DataTransformer__clean_transactions_df()

    cleaned_df = data_transformer.transactions_df

    assert len(cleaned_df) == 1

    remaining_ids = set(cleaned_df["transaction_id"])
    assert remaining_ids == {"1"}


def test_normalise_transactions_df_creates_row_for_each_item():
    data = [
        {
            "transaction_id": "0",
            "user_id": 11,
            "timestamp": "2025-03-18T00:25:53",
            "items": [
                {"product_id": 8, "quantity": 7},
                {"product_id": 14, "quantity": 8},
                {"product_id": 15, "quantity": 13},
                {"product_id": 17, "quantity": 10},
                {"product_id": 13, "quantity": 15},
            ],
            "status": "RETURNED",
        },
        {
            "transaction_id": "1",
            "user_id": 4,
            "timestamp": "2023-12-14T16:54:16",
            "items": [
                {"product_id": 14, "quantity": 8},
                {"product_id": 9, "quantity": 15},
                {"product_id": 17, "quantity": 3},
                {"product_id": 4, "quantity": 3},
            ],
            "status": "COMPLETED",
        },
        {
            "transaction_id": "2",
            "user_id": 8,
            "timestamp": "2024-07-05T18:34:33",
            "items": [
                {"product_id": 18, "quantity": 8},
                {"product_id": 4, "quantity": 10},
            ],
            "status": "CANCELLED",
        },
    ]

    data_transformer = DataTransformer()
    data_transformer.transactions_df = pd.DataFrame(data)
    data_transformer._DataTransformer__normalise_transactions_df()
    normalised_df = data_transformer.transactions_df

    assert len(normalised_df) == 11

    assert "product_id" in list(normalised_df.columns)
    assert "quantity" in list(normalised_df.columns)


def test_merge_result_df_merges_correctly():
    users_data = [
        {"user_id": 0, "name": "Gabriela Karamazov", "country": "USA"},
        {"user_id": 1, "name": "Ivan Andrews", "country": "Spain"},
        {"user_id": 2, "name": "Anya Peterson", "country": "Ireland"},
    ]

    products_data = [
        {"product_id": "0", "category": "Cameras", "price": 679.98},
        {"product_id": "1", "category": "Smartphones", "price": 990.1},
        {"product_id": "2", "category": "Tablets", "price": 500.55},
    ]

    transactions_data = [
        {
            "transaction_id": "0",
            "user_id": 0,
            "timestamp": "2025-03-18T00:25:53",
            "items": [
                {"product_id": 2, "quantity": 7},
                {"product_id": 0, "quantity": 8},
            ],
            "status": "RETURNED",
        },
        {
            "transaction_id": "1",
            "user_id": 1,
            "timestamp": "2023-12-14T16:54:16",
            "items": [{"product_id": 2, "quantity": 8}],
            "status": "COMPLETED",
        },
        {
            "transaction_id": "2",
            "user_id": 2,
            "timestamp": "2024-07-05T18:34:33",
            "items": [
                {"product_id": 0, "quantity": 8},
                {"product_id": 1, "quantity": 10},
            ],
            "status": "CANCELLED",
        },
    ]

    data_transformer = DataTransformer()
    data_transformer.users_df = pd.DataFrame(users_data)
    data_transformer.products_df = pd.DataFrame(products_data)
    data_transformer.transactions_df = pd.DataFrame(transactions_data)

    data_transformer._DataTransformer__normalise_transactions_df()

    assert data_transformer._DataTransformer__merge_result_df() is True

    result_df = data_transformer.result

    assert list(result_df.columns) == [
        "transaction_id",
        "timestamp",
        "status",
        "product_id",
        "category",
        "quantity",
        "price",
        "total_item_value",
        "user_id",
        "name",
        "country",
    ]
