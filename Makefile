.PHONY: all

DB:=2.sqlify/open-access-is-great-but-where-are-the-images.db

all: $(DB)

$(DB):
	python3 2.sqlify/sqlify.py
