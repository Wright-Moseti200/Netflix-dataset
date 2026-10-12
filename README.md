# Netflix Titles — Exploratory Data Analysis

Analysis of ~8,800 Netflix movies and TV shows (`netflix_titles.csv`, up to Sept 2021).

## Questions answered

1. Top genres (`listed_in`) by type — Movies: Dramas / International Movies, Documentaries, Stand-Up Comedy. TV Shows: Kids' TV, International TV Dramas.
2. Top countries by type — US dominates both; India #2 for movies; UK #2 for TV shows.
3. Titles added per year (`date_added`) — steep growth 2015–2019 (peak 2,016 in 2019), dip in 2020–2021.
4. Top ratings by type — TV-MA and TV-14 lead for both movies and TV shows.
5. Movie durations (`duration`) — mean ~100 min, median 98 min; most films fall in the 91–120 min band.

## Project structure

```
.
├── netflix_titles.csv          # source dataset (show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)
├── analysis.ipynb              # main notebook: cleaning + Q1–Q5 + matplotlib charts
├── src/netflix_dataset/__init__.py  # same analysis as an importable script
├── pyproject.toml / uv.lock    # deps (requires-python >=3.12)
```

## Data cleaning (`analysis.ipynb`, `src/netflix_dataset/__init__.py:8-21`)

- Drop columns with >50% missing; fill numeric NaNs with median (skewed) or mean, categorical with `"Missing"`.
- `drop_duplicates()`.
- Fixes: parse year from `date_added` (`__init__.py:46`), filter bogus `rating` values (`74 min`, `84 min`, `66 min`), parse movie minutes from `duration` and bin into `<=60 / 61-90 / 91-120 / 121-150 / 150+`.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python >= 3.12.

```bash
uv sync
```

## Usage

Notebook:

```bash
uv run jupyter notebook analysis.ipynb
```

Script version (prints summaries, opens matplotlib windows):

```bash
uv run python -c "import netflix_dataset"
```

## Dependencies

- `pandas` — loading, cleaning, groupby/value_counts
- `matplotlib` — barh / line / bar / hist charts (helper `plot_top_by_type`, `__init__.py:24-33`)
- `ipykernel` — notebook kernel
