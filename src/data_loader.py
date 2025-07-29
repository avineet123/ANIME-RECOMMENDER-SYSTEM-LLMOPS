import pandas as pd


class AnimeDataLoader:
    def __init__(self, original_csv: str, processed_csv: str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self):
        # Load the dataset
        df = pd.read_csv(self.original_csv, encoding="utf-8", on_bad_lines="skip").dropna()

        # Ensure required columns exist
        required_cols = {"Name", "Genres", "sypnopsis"}  # fix to "synopsis" if needed
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing Columns in CSV file: {missing_cols}")

        # Create a combined info string
        df["combine_info"] = (
            "Title: " + df["Name"] +
            " Overview: " + df["sypnopsis"] +
            " Genres: " + df["Genres"]
        )

        # Save the processed CSV with just the combined info
        df[["combine_info"]].to_csv(self.processed_csv, index=False, encoding="utf-8")

        return self.processed_csv
