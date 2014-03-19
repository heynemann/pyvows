vows test:
	@env PYTHONPATH=. python pyvows/cli.py --cover --cover-package=pyvows --cover-threshold=80.0 --profile tests/

ci_test: setup
	@env PYTHONPATH=. python pyvows/cli.py --cover --cover-package=pyvows --cover-threshold=80.0 --cover-report=pyvows.coverage.xml -x tests/

setup:
	@pip install --upgrade --editable .\[tests\]

publish:
	python setup.py sdist upload

.PHONY: vows test setup publish ci_test
