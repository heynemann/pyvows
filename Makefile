vows:
	@env PYTHONPATH=. python pyvows/console.py --cover --cover_package=pyvows --cover_package=pyvows.assertions --cover_threshold=80.0 tests/

test:
	@nosetests -s -v tests/

setup:
	@pip install --requirement=REQUIREMENTS
