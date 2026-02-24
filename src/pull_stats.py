# importing dependencies
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from pybaseball import statcast

# argparse method
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pull statcast data and save raw parquet file.")
    parser.add_argument("--force", action="store_true", 
                        help="If it already exists, re-download and overwrite existing parquet raw data file.")
    return parser.parse_args()

def main() -> None:
    #shoutout argparser
    args = parse_args()

    # local file paths
    OUTPUT_PATH = Path("../data/raw/statcast_2024_raw.parquet")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if OUTPUT_PATH.exists() and not args.force:
        print(f"Raw file already exists: {OUTPUT_PATH}")
        print("Re-Run with --force to re-download.")
        return
    
    # pulling statcast data 
    start_date = "2024-03-28"
    end_date = "2024-09-29"
    df = statcast(start_date, end_date)
    print("Saving raw data to parquet file...")
    df.to_parquet(OUTPUT_PATH, index=False)

    # Sanity checks - Extracting necessary columns and making sure they exist in the dataset
    key_cols = ["pitch_type", "description", "p_throws",
            "release_speed", "release_spin_rate",
            "pfx_x", "pfx_z"]
    aqui = [c for c in key_cols if c in df.columns]
    
    if aqui:
        print("\nPreview key columns:")
        print(df[aqui].head(20).to_string(index=False))
    else: 
        print("\nNone of the key columns were found.")

    if "pitch_type" in df.columns:
        print("\nTop pitch types:")
        print(df["pitch_type"].value_counts().head(12).to_string())
    
    # Checking only for movement, velocity, and spin rate. This is the core data. 
    missing_cols = [c for c in ["pfx_x", "pfx_z", "release_speed", "release_spin_rate"] if c in df.columns]
    if missing_cols:
        print("\nMissingness rates (fraction NA):")
        print(df[missing_cols].isna().mean().to_string())

if __name__ == "__main__":
    main()

