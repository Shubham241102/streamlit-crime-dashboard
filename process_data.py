import pandas as pd

# Define file paths
INPUT_FILE = 'data/chicago_crimes.csv'
OUTPUT_FILE = 'data/chicago_crimes_processed.csv'

print("Loading data...")
df = pd.read_csv(INPUT_FILE)

print("Cleaning data...")
# Keep only necessary columns
df = df[['Date', 'Primary Type', 'Latitude', 'Longitude']]
# Drop rows with no location data
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
# Convert 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# Drop rows where date conversion failed
df.dropna(subset=['Date'], inplace=True)

# Take a sample if the dataset is too large
if len(df) > 100000:
    print("Sampling data to 100,000 rows...")
    df = df.sample(n=100000, random_state=42)

print(f"Saving processed data to {OUTPUT_FILE}...")
df.to_csv(OUTPUT_FILE, index=False)

print("Done!")