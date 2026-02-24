# import dependencies
import pandas as pd 
from pathlib import Path

# file paths
RAW_DATA = "../data/raw/statcast_2024_raw.parquet"
CLEANED_DATA = "../data/interim/statcast_2024_cleaned.parquet"

# constants
MIN_PITCHES = 500
MAJOR_PITCH_TYPES = ["FF","SI","SL","CH","FC","ST","CU","FS","KC"]

def main() -> None: 
    # loading raw data
    df = pd.read_parquet(RAW_DATA)

    # counting only reg. season 
    if "game_type" in df.columns: 
        df = df[df["game_type"] == "R"]
    
    # remove missing core data
    needed = ["pfx_x", "pfx_z", "release_speed", "release_spin_rate"]
    present_needed = [c for c in needed if c in df.columns]
    df = df.dropna(subset=present_needed)

    # keep major pitch types
    if "pitch_type" in df.columns: 
        df = df[df["pitch_type"].isin(MAJOR_PITCH_TYPES)]

    # remove pitchers/pos. players who did not throw significant pitches 
    if "pitcher" in df.columns:
        pitch_counts = df.groupby("pitcher").size()
        valid_pitchers = pitch_counts[pitch_counts >= MIN_PITCHES].index
        df = df[df["pitcher"].isin(valid_pitchers)]

    # print outputted filtered data
    print("Wrote:", CLEANED_DATA)
    print("Shape:", df.shape)
    if "pitch_type" in df.columns:
        print("Pitch type counts (top 10):")
        print(df["pitch_type"].value_counts().head(10).to_string())

if __name__ == "__main__":
    main()