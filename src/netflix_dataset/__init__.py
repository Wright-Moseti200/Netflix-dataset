import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")

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

# helper: draws the top 5 per type as two side-by-side bar charts
def plot_top_by_type(counts, title):
    top = counts.groupby(level=0).head(5)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, t in zip(axes, ["Movie", "TV Show"]):
        top.loc[t].sort_values().plot(kind="barh", ax=ax, title=t)
        ax.set_ylabel("")
        ax.set_xlabel("Number of titles")
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

# Q1: genres
counts = df.groupby("type")["listed_in"].value_counts()
print(counts.groupby(level=0).head(5))
plot_top_by_type(counts, "Top genres by type")

# Q2: countries
counts2 = df.groupby("type")["country"].value_counts()
print(counts2.groupby(level=0).head(5))
plot_top_by_type(counts2, "Top countries by type")

# Q3: titles added per year
df["dates"] = df["date_added"].str.strip().str.split(" ").str.get(2)
count3 = df.groupby("dates")["title"].count()
print(count3)

count3.plot(kind="line", marker="o", title="Titles added to Netflix per year")
plt.xlabel("Year added")
plt.ylabel("Number of titles")
plt.show()

# Q4: ratings
bad = ["Missing", "74 min", "84 min", "66 min"]
df_rating = df[~df["rating"].isin(bad)]

count4 = df_rating.groupby("type")["rating"].value_counts()
print(count4.groupby(level=0).head(5))
plot_top_by_type(count4, "Top ratings by type")

# Q5: movie durations
movies = df[(df["type"]=="Movie")]
movies["minutes"] = pd.to_numeric(movies["duration"].str.split(" ").str.get(0),errors="coerce")
movies["length_band"] = pd.cut(
    movies["minutes"],
    bins=[0, 60, 90, 120, 150, 400],
    labels=["<=60", "61-90", "91-120", "121-150", "150+"],
)
print(movies["length_band"].value_counts())
print(movies["minutes"].describe())

movies["length_band"].value_counts().sort_index().plot(kind="bar", title="Movies by length band")
plt.ylabel("Number of movies")
plt.show()

movies["minutes"].plot(kind="hist", bins=30, title="Distribution of movie length")
plt.xlabel("Minutes")
plt.show()