# Makefile
.PHONY: install test test-headless clean allure-report

install:
	pip install -r requirements.txt

test:
	pytest tests/ --alluredir=reports/allure-results

test-headless:
	HEADLESS=True pytest tests/ --alluredir=reports/allure-results

clean:
	rm -rf reports/*
	rm -rf __pycache__/
	rm -rf .pytest_cache/

allure-report:
	allure generate reports/allure-results --clean -o reports/allure-report
	allure open reports/allure-report
