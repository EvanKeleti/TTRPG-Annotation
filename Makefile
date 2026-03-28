.PHONY: setup label parse-data

setup:
	uv sync
	uv run label-studio init TTRPG-Annotations --label-config config.xml

label:
	uv run label-studio

parse-data: scripts/parse_data.py
	uv run scripts/parse_data.py | less
