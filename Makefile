.PHONY: parse-data

parse-data: samples.json

samples.json: scripts/parse_data.py
	uv run scripts/parse_data.py | less
