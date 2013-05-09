TEST_PREFIX = @env PYTHONPATH=. python pyvows/ --cover --cover-package=pyvows --cover-threshold=80.0

vows test:
	$(TEST_PREFIX) --profile tests/

ci_test:
	$(TEST_PREFIX) -r pyvows.coverage.xml -x tests/

setup:
	@pip install --requirement=REQUIREMENTS

publish:
	python setup.py sdist upload

.PHONY: vows test setup publish ci_test
