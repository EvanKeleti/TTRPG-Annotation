.PHONY: setup label parse-data

setup:
	uv run label-studio start TTRPG-Annotations --init --label-config config.xml

label:
	uv run label-studio

parse-data: scripts/parse_data.py
	uv run scripts/parse_data.py | less
