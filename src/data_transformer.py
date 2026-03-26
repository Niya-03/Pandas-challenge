import pandas as pd
import os
import json
from config import (
    USERS_FILEPATH,
    PRODUCTS_FILEPATH,
    TRANSACTIONS_FILEPATH,
    CLEANED_DATASET_FILEPATH,
    INVALID_TIMESTAMP_LOG_FILEPATH,
)


class DataTransformer:
    def __init__(self):
        pass

    def __create_dataframes(self) -> bool:
        try:
            if not os.path.exists(USERS_FILEPATH):
                return False

            if not os.path.exists(PRODUCTS_FILEPATH):
                return False

            if not os.path.exists(TRANSACTIONS_FILEPATH):
                return False

            self.users_df = pd.read_json(USERS_FILEPATH)
            self.products_df = pd.read_json(PRODUCTS_FILEPATH)
            self.transactions_df = pd.read_json(TRANSACTIONS_FILEPATH)

            return True
        except Exception as e:
            print(f"Error creating dataframes: {e}")
            return False

    def __clean_products_df(self) -> None:
        self.products_df = self.products_df.dropna()

    def __log(self, data_to_log: pd.DataFrame) -> None:
        try:
            log_dict = data_to_log.to_dict(orient="records")

            with open(INVALID_TIMESTAMP_LOG_FILEPATH, "w") as f:
                json.dump(log_dict, f, indent=4)

        except Exception as e:
            print(f"Error logging transactions with invalid timestamps: {e}")

    def __clean_transactions_df(self) -> bool:
        try:

            timestamp_validity = pd.to_datetime(
                self.transactions_df["timestamp"], errors="coerce"
            )

            invalid_timestamps_transactions_df = self.transactions_df[
                timestamp_validity.isna()
            ]
            self.__log(
                invalid_timestamps_transactions_df,
            )

            transactions_df_clean = self.transactions_df[timestamp_validity.notna()]
            transactions_df_clean = transactions_df_clean.reset_index(drop=True)

            transactions_df_clean = transactions_df_clean[
                transactions_df_clean["items"].apply(
                    lambda x: isinstance(x, list) and len(x) > 0
                )
            ]
            transactions_df_clean = transactions_df_clean.reset_index(drop=True)

            self.transactions_df = transactions_df_clean

            return True
        except Exception as e:
            print(f"Error while cleaning transactions_df: {e}")
            return False

    def __normalise_transactions_df(self) -> bool:
        try:
            normalised_transactions_df = self.transactions_df.explode("items")
            normalised_items = pd.json_normalize(normalised_transactions_df["items"])
            normalised_transactions_df = normalised_transactions_df.drop(
                columns=["items"]
            ).reset_index(drop=True)
            normalised_transactions_df = pd.concat(
                [normalised_transactions_df, normalised_items], axis=1
            )
            self.transactions_df = normalised_transactions_df

            return True
        except Exception as e:
            print(f"Error while normalising transactions_df: {e}")
            return False

    def __merge_result_df(self) -> bool:
        try:
            self.products_df["product_id"] = self.products_df["product_id"].astype(int)
            self.transactions_df["product_id"] = self.transactions_df[
                "product_id"
            ].astype(int)

            merged_transactions_users_df = self.transactions_df.merge(
                self.users_df, on="user_id"
            )
            merged_full_df = merged_transactions_users_df.merge(
                self.products_df, on="product_id"
            )
            merged_full_df["total_item_value"] = (
                merged_full_df["price"] * merged_full_df["quantity"]
            )
            merged_full_df = merged_full_df[
                [
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
            ]

            self.result = merged_full_df

            return True
        except Exception as e:
            print(f"Error while merging results: {e}")
            return False

    def generate_clean_data_csv(self) -> bool:
        if not self.__create_dataframes():
            return False

        self.__clean_products_df()

        if not self.__clean_transactions_df():
            return False

        if not self.__normalise_transactions_df():
            return False

        if not self.__merge_result_df():
            return False

        self.result.to_csv(CLEANED_DATASET_FILEPATH, index=False)

        return True
