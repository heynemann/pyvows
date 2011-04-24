vows:
	@env PYTHONPATH=. python pyvows/__init__.py tests/

test:
	@nosetests -s -v tests/

setup:
	@pip install --requirement=REQUIREMENTS
