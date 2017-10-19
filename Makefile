test:
	@env PYTHONPATH=. python pyvows/cli.py --cover --cover-package=pyvows --cover-threshold=80.0 --profile tests/

coverage:
	@env PYTHONPATH=. python pyvows/cli.py --cover --cover-package=pyvows --cover-threshold=80.0 --cover-report=coverage.xml -x tests/

publish:
	python setup.py sdist upload

.PHONY: test coverage publish
