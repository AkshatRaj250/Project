import pandas as pd

def analyze_data(data):
    if not data:
        return "No data available"

    df = pd.DataFrame(data)

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    # Analysis
    avg_weight = df["weight"].mean()
    max_weight = df.groupby("exercise")["weight"].max()
    total_workouts = len(df)

    result = f"""
Average Weight: {avg_weight:.2f}
Total Workouts: {total_workouts}

Max Weight per Exercise:
{max_weight}
"""
    return result