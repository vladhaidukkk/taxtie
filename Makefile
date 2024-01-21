install:
	@pip install -r requirements.txt -r requirements-dev.txt

compile:
	@rm -rf requirements*.txt
	@pip-compile requirements.in
	@pip-compile requirements-dev.in

sync:
	@pip-sync requirements*.txt
