install-deps:
	@pip install -r requirements.txt

lock-deps:
	@pip-compile --upgrade --output-file=requirements.txt
	@pip-compile --extra dev --upgrade --output-file=requirements-dev.txt

sync-deps:
	@pip-sync requirements-dev.txt
