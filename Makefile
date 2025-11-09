.PHONY: help install test test-chrome test-firefox test-headless report clean

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run tests in Chrome"
	@echo "  make test-chrome   - Run tests in Chrome"
	@echo "  make test-firefox  - Run tests in Firefox"
	@echo "  make test-headless - Run tests in headless Chrome"
	@echo "  make test-single TEST=test_name - Run specific test"
	@echo "  make test-01       - Run test_01_home_page_loads"
	@echo "  make test-02       - Run test_02_careers_page_navigation"
	@echo "  make test-03       - Run test_03_filter_qa_jobs"
	@echo "  make test-04       - Run test_04_verify_job_listings"
	@echo "  make test-05       - Run test_05_view_role_lever_redirect"
	@echo "  make test-06       - Run test_06_complete_e2e_flow"
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

# Individual test shortcuts
test-01:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py::TestInsiderCareers::test_01_home_page_loads --browser=chrome --alluredir=reports/allure-results -v -s

test-02:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py::TestInsiderCareers::test_02_careers_page_navigation_and_blocks --browser=chrome --alluredir=reports/allure-results -v -s

test-03:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py::TestInsiderCareers::test_03_filter_qa_jobs --browser=chrome --alluredir=reports/allure-results -v -s

test-04:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py::TestInsiderCareers::test_04_verify_job_listings_criteria --browser=chrome --alluredir=reports/allure-results -v -s

test-05:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py::TestInsiderCareers::test_05_view_role_lever_redirect --browser=chrome --alluredir=reports/allure-results -v -s

test-06:
	mkdir -p screenshots reports/allure-results
	pytest tests/test_insider_careers.py::TestInsiderCareers::test_06_complete_e2e_flow --browser=chrome --alluredir=reports/allure-results -v -s

report:
	allure serve reports/allure-results

clean:
	rm -rf screenshots/* reports/* test_execution.log .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true