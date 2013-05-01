vows test:
	@env PYTHONPATH=. python pyvows/cli.py --cover --cover-package=pyvows --cover-package=pyvows.assertions --cover-package=pyvows.reporting --cover-package=pyvows.runner --cover-threshold=80.0 --profile tests/

ci_test:
	@env PYTHONPATH=. python pyvows/cli.py --cover --cover-package=pyvows --cover-package=pyvows.assertions --cover-package=pyvows.reporting --cover-package=pyvows.runner --cover-threshold=80.0 -r pyvows.coverage.xml -x tests/

setup:
	@pip install --requirement=REQUIREMENTS

publish:
	python setup.py sdist upload

.PHONY: vows test setup publish ci_test
