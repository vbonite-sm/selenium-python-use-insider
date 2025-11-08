.PHONY: help install test test-chrome test-firefox test-headless report clean

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run tests in Chrome"
	@echo "  make test-chrome   - Run tests in Chrome"
	@echo "  make test-firefox  - Run tests in Firefox"
	@echo "  make test-headless - Run tests in headless Chrome"
	@echo "  make report        - Generate and view Allure report"
	@echo "  make clean         - Clean generated files"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test: test-chrome

test-chrome:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py --browser=chrome --alluredir=reports/allure-results -v

test-firefox:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py --browser=firefox --alluredir=reports/allure-results -v

test-headless:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py --browser=chrome --headless=true --alluredir=reports/allure-results -v

report:
	allure serve reports/allure-results

clean:
	rm -rf screenshots/* reports/* test_execution.log .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true