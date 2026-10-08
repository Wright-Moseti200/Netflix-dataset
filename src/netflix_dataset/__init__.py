import pandas as pd

df = pd.read_csv("netflix_titles.csv")

# few gaps in columns that need parsing later: drop those rows
df = df.dropna(subset=["date_added", "rating", "duration"])

for col, val in df.isna().sum().items():
    if val == 0:
        continue
    elif val > len(df) * 0.5:
        df = df.drop(columns=col)                     
    elif pd.api.types.is_numeric_dtype(df[col]):
        if abs(df[col].skew()) > 1:
            df[col] = df[col].fillna(df[col].median())  
        else:
            df[col] = df[col].fillna(df[col].mean())    
    else:
        df[col] = df[col].fillna("Missing")            

df = df.drop_duplicates()
print(df.isna().sum())
