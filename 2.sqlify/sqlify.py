#!/usr/bin/env python3


import argparse
import csv
import os.path
import sqlite3


HERE = os.path.dirname(__file__)


BASE_DIR = os.path.join(HERE, "..")


IMAGES_DB_PATH = os.path.join(HERE, "open-access-is-great-but-where-are-the-images.db")


CREATE_MET_IMAGES_SQL = f"""
CREATE TABLE IF NOT EXISTS met_images (
    `object_id` INTEGER NOT NULL,
    `image_url` TEXT NOT NULL
)
"""


CREATE_MET_IMAGES_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS `met_images_object_id_idx`
ON `met_images` (`object_id`)
"""


CREATE_CHICAGO_IMAGES_SQL = f"""
CREATE TABLE IF NOT EXISTS chicago_images (
    `object_name` VARCHAR(255) NOT NULL,
    `image_url` TEXT NOT NULL
)
"""


CREATE_CHICAGO_IMAGES_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS `chicago_images_object_id_idx`
ON `chicago_images` (`object_name`)
"""



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default=IMAGES_DB_PATH)
    parser.add_argument("--exclude-indices", action="store_true")
    args = parser.parse_args()

    with sqlite3.connect(args.db_path) as conn:
        curs = conn.cursor()

        curs.execute(CREATE_MET_IMAGES_SQL)

        with open(os.path.join(BASE_DIR, "1.data", "met-images.csv"), "r") as fi:
            curs.executemany("INSERT OR IGNORE INTO met_images VALUES (?, ?)", csv.reader(fi))

        curs.execute(CREATE_CHICAGO_IMAGES_SQL)

        if not args.exclude_indices:
            curs.execute(CREATE_MET_IMAGES_INDEX_SQL)
            curs.execute(CREATE_CHICAGO_IMAGES_INDEX_SQL)

        with open(os.path.join(BASE_DIR, "1.data", "chicago-images.csv"), "r") as fi:
            curs.executemany("INSERT OR IGNORE INTO chicago_images VALUES (?, ?)", csv.reader(fi))


    with sqlite3.connect(IMAGES_DB_PATH) as conn:
        conn.execute("VACUUM")
