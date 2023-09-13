black: 
	poetry run black .
	poetry run black --check .

autopep8:
	poetry run autopep8 -r -i src tests

flake8:
	poetry run flake8
