# import dependencies
import pandas as pd

# define swings
SWING_EVENTS = ["swinging_strike",
    "swinging_strike_blocked",
    "foul",
    "foul_tip",
    "hit_into_play",
    "hit_into_play_no_out",
    "hit_into_play_score",]

# define whiffs
WHIFF_EVENTS= ["swinging_strike","swinging_strike_blocked",]

# swing vs whiff labeling function
def label_swings_and_whiffs(df: pd.DataFrame) -> pd.DataFrame:
    df["is_swing"] = df["description"].isin(SWING_EVENTS)
    df["is_whiff"] = df["description"].isin(WHIFF_EVENTS)
    return df