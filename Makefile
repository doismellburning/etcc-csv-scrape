CODEDIRS=transform.py test

.DEFAULT_GOAL := check

.PHONY: bootstrap
bootstrap:
	uv sync --dev

.PHONY: check
check: format lint ty

.PHONY: format
format:
	uv run ruff format --check $(CODEDIRS)

.PHONY: lint
lint:
	uv run ruff check $(CODEDIRS)

.PHONY: ty
ty:
	uv run ty check

.PHONY: fix
fix:
	uv run ruff format $(CODEDIRS)
	uv run ruff check --fix $(CODEDIRS)

.PHONY: clean
clean:
	git clean -X --force

.PHONY: test
test:
	uv run coverage run --source transform --module pytest test
	uv run coverage report
	uv run coverage html

packetlist.csv:
	curl https://ukrepeater.net/csvcreate4.php > packetlist.csv

packetlist.json: packetlist.csv transform.py Makefile
	uv run python3 transform.py packetlist.csv packetlist.json
