import pandas as pd
from config import CLEANED_DATASET_FILEPATH, REPORT_FILEPATH
import json

class ReportGenerator:
    def __init__(self):
        self.results = []

    def __generate_revenue_by_category(self) -> bool:
        try:
            df_filtered_category = self.cleaned_df[
                self.cleaned_df["status"] == "COMPLETED"
            ]
            category_result = (
                df_filtered_category.groupby("category")["total_item_value"]
                .sum()
                .reset_index()
            )
            result_dict = category_result.to_dict(orient="records")
            self.results.append(result_dict)

            return True

        except Exception as e:
            print(f"Error while generating revenue by category: {e}")
            return False

    def __generate_top_spenders(self) -> bool:
        try:
            user_result = (
                self.cleaned_df.groupby("user_id")["total_item_value"]
                .sum()
                .reset_index()
            )
            user_result = user_result.sort_values(
                by="total_item_value", ascending=False
            )
            user_result = user_result.merge(
                self.cleaned_df[["user_id", "name"]].drop_duplicates("user_id"), on="user_id", how="left"
            )

            user_dict = user_result.head(3).to_dict(orient="records")

            self.results.append(user_dict)

            return True

        except Exception as e:
            print(f"Error while generating top spenders: {e}")
            return False

    def __generate_return_rate(self) -> bool:
        try:
            total_items_per_country = (
                self.cleaned_df.groupby("country")["quantity"].sum().reset_index()
            )
            total_items_per_country.rename(
                columns={"quantity": "total_sold_items"}, inplace=True
            )

            df_filtered_status = self.cleaned_df[
                self.cleaned_df["status"] == "RETURNED"
            ]
            total_returned_items_per_country = (
                df_filtered_status.groupby("country")["quantity"].sum().reset_index()
            )
            total_returned_items_per_country.rename(
                columns={"quantity": "total_returned_items"}, inplace=True
            )

            return_rate_result = total_items_per_country.merge(
                total_returned_items_per_country, on="country"
            )
            return_rate_result["return_rate"] = (
                return_rate_result["total_returned_items"]
                / return_rate_result["total_sold_items"]
            )
            return_rate_result = return_rate_result[["country", "return_rate"]]

            return_rate_dict = return_rate_result.to_dict(orient="records")
            self.results.append(return_rate_dict)

            return True
        except Exception as e:
            print(f"Error while generating return rate: {e}")
            return False

    def generate_report(self) -> bool:
        self.cleaned_df = pd.read_csv(CLEANED_DATASET_FILEPATH)

        if not self.__generate_revenue_by_category():
            return False

        if not self.__generate_top_spenders():
            return False

        if not self.__generate_return_rate():
            return False

        with open(REPORT_FILEPATH, "w") as f:
                json.dump(self.results, f, indent=4)

        return True
