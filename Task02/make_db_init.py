import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SQL_OUT = ROOT / "db_init.sql"


def quote_value(val):
    if val is None:
        return "NULL"
    return "'" + str(val).replace("'", "''") + "'"


def stream_csv(name):
    with open(ROOT / name, encoding="utf-8", newline="") as fh:
        for rec in csv.DictReader(fh):
            yield rec


def stream_users():
    with open(ROOT / "users.txt", encoding="utf-8") as fh:
        for raw in fh:
            cols = raw.rstrip("\n").split("|")
            if len(cols) == 6:
                yield cols


def split_title(title):
    found = re.search(r"\((\d{4})\)\s*$", title)
    if found:
        return title[:found.start()].rstrip(), int(found.group(1))
    return title, None


def build_sql():
    with open(SQL_OUT, "w", encoding="utf-8", newline="\n") as out:
        out.write("PRAGMA foreign_keys = OFF;\n\n")

        out.write("DROP TABLE IF EXISTS users;\n")
        out.write("DROP TABLE IF EXISTS tags;\n")
        out.write("DROP TABLE IF EXISTS ratings;\n")
        out.write("DROP TABLE IF EXISTS movies;\n\n")

        out.write("""CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title VARCHAR(158),
    year INTEGER,
    genres VARCHAR(77)
);

""")

        out.write("""CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    rating DECIMAL(3,1),
    timestamp INTEGER
);

""")

        out.write("""CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    tag VARCHAR(85),
    timestamp INTEGER
);

""")

        out.write("""CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(22),
    email VARCHAR(32),
    gender VARCHAR(6),
    register_date DATE,
    occupation VARCHAR(13)
);

""")

        out.write("BEGIN TRANSACTION;\n\n")

        for rec in stream_csv("movies.csv"):
            clean_title, year = split_title(rec["title"])
            out.write(
                "INSERT INTO movies (id, title, year, genres) VALUES "
                f"({int(rec['movieId'])}, {quote_value(clean_title)}, "
                f"{year if year is not None else 'NULL'}, {quote_value(rec['genres'])});\n"
            )

        for counter, rec in enumerate(stream_csv("ratings.csv"), start=1):
            out.write(
                "INSERT INTO ratings "
                "(id, user_id, movie_id, rating, timestamp) VALUES "
                f"({counter}, {int(rec['userId'])}, {int(rec['movieId'])}, "
                f"{rec['rating']}, {int(rec['timestamp'])});\n"
            )

        for counter, rec in enumerate(stream_csv("tags.csv"), start=1):
            out.write(
                "INSERT INTO tags "
                "(id, user_id, movie_id, tag, timestamp) VALUES "
                f"({counter}, {int(rec['userId'])}, {int(rec['movieId'])}, "
                f"{quote_value(rec['tag'])}, {int(rec['timestamp'])});\n"
            )

        for cols in stream_users():
            uid, name, email, gender, reg_date, occ = cols
            out.write(
                "INSERT INTO users "
                "(id, name, email, gender, register_date, occupation) VALUES "
                f"({int(uid)}, {quote_value(name)}, {quote_value(email)}, "
                f"{quote_value(gender)}, {quote_value(reg_date)}, "
                f"{quote_value(occ)});\n"
            )

        out.write("\nCOMMIT;\n")


if __name__ == "__main__":
    build_sql()
    print(f"SQL script created: {SQL_OUT}")