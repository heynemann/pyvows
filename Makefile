vows:
	@env PYTHONPATH=. python pyvows/console.py tests/

test:
	@nosetests -s -v tests/

setup:
	@pip install --requirement=REQUIREMENTS
