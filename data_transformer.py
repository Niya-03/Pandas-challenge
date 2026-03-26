import pandas as pd
import os
from config import (
    USERS_FILENAME,
    PRODUCTS_FILENAME,
    TRANSACTIONS_FILENAME,
    CLEANED_DATASET_FILENAME,
)


class DataTransformer:
    def __init__():
        pass

    def __create_dataframes(self):
        if not os.path.exists(USERS_FILENAME):
            return False

        if not os.path.exists(PRODUCTS_FILENAME):
            return False

        if not os.path.exists(TRANSACTIONS_FILENAME):
            return False

        self.users_df = pd.read_json(USERS_FILENAME)
        self.products_df = pd.read_json(PRODUCTS_FILENAME)
        self.transactions_df = pd.read_json(TRANSACTIONS_FILENAME)

    def __clean_products_df(self):
        self.products_df = self.products_df.dropna()

    def __log(data_to_log, log_filename):
        data_to_log.to_json(log_filename, index=False)

    def __clean_transactions_df(self):
        try:
            timestamp_validity = pd.to_datetime(
                self.transactions_df["timestamp"], errors="coerce"
            )

            invalid_timestamps_transactions_df = self.transactions_df[
                timestamp_validity.isna()
            ]
            self.__log(
                invalid_timestamps_transactions_df,
                "invalid_timestamp_transactions.json",
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

    def __normalise_transactions_df(self):
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

    def __merge_result_df(self):
        try:
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

    def generate_clean_data_csv(self):
        if not self.__create_dataframes():
            return False

        if not self.__clean_products_df():
            return False

        if not self.__clean_transactions_df():
            return False

        if not self.__normalise_transactions_df():
            return False

        if not self.__merge_result_df():
            return False

        self.result.to_csv(CLEANED_DATASET_FILENAME, index=False)

        return True
