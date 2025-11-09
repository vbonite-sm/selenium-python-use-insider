# Insider QA Test Automation Framework

Selenium Python test automation framework for Insider QA assessment.

## Architecture

- **Framework**: Selenium + Python + Pytest
- **Design Patterns**: Repository Pattern, Loadable Component Pattern, Page Object Model, Decorator Pattern
- **Reporting**: Allure Reports
- **CI/CD**: GitHub Actions

## Prerequisites

- Python 3.11+
- Git
- Chrome / Firefox browser
- Allure (for reports)

## Quick Start
```bash
# Clone repository
git clone https://github.com/vbonite-sm/selenium-python-use-insider
cd selenium-python-use-insider

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Git Bash

# Install dependencies
make install

# Run tests
make test

# View report
make report
```

## Available Commands
```bash
make help           # Show all available commands
make install        # Install dependencies
make test           # Run tests in Chrome
make test-chrome    # Run tests in Chrome
make test-firefox   # Run tests in Firefox
make test-headless  # Run tests in headless Chrome
make report         # Generate and view Allure report
make clean          # Clean generated files
```

## Manual Test Execution

If not using Makefile:
```bash
# Chrome
pytest tests/test_insider_careers.py --browser=chrome --alluredir=reports/allure-results -v

# Firefox
pytest tests/test_insider_careers.py --browser=firefox --alluredir=reports/allure-results -v

# Headless
pytest tests/test_insider_careers.py --browser=chrome --headless=true --alluredir=reports/allure-results -v

# Specific test
pytest tests/test_insider_careers.py::TestInsiderCareers::test_06_complete_e2e_flow -v
```

## Project Structure
```
selenium-python-use-insider/
├── .github/workflows/        # CI/CD pipeline
├── config/                   # Framework configuration
├── locators/                 # JSON-based locator repository
├── pages/                    # Page Object Models
├── tests/                    # Test cases (AAA pattern)
├── utils/                    # Decorators and helpers
├── conftest.py              # Pytest fixtures
├── pytest.ini               # Pytest configuration
├── Makefile                 # Build commands
└── README.md
```

## Test Scenarios

| Test | Description |
|------|-------------|
| `test_01_home_page_loads` | Verify home page loads |
| `test_02_careers_page_navigation_and_blocks` | Navigate to Careers and verify blocks |
| `test_03_filter_qa_jobs` | Filter QA jobs by location and department |
| `test_04_verify_job_listings_criteria` | Verify all jobs meet criteria |
| `test_05_view_role_lever_redirect` | Verify redirect to Lever application |
| `test_06_complete_e2e_flow` | Complete end-to-end test |

## CI/CD

Tests run automatically on push to `main`. Manual trigger available in GitHub Actions.

Reports deployed to: `https://<your-username>.github.io/<repo-name>/`

## Configuration

Edit `config/config.py` to modify:
- Browser settings
- Timeouts
- Screenshot settings
- Reporting options

## Key Design Patterns

- **Repository Pattern** - Locators in JSON, easy maintenance
- **Loadable Component** - Pages validate before use
- **AAA Pattern** - Clear test structure (Arrange-Act-Assert)
- **Decorator Pattern** - Automatic logging and screenshots

## Troubleshooting

**Virtual environment not activated:**
```bash
source venv/Scripts/activate
```

**Dependencies missing:**
```bash
make install
```

**Clear cache:**
```bash
make clean
```

**Allure not installed:**
```bash
scoop install allure  # Windows
brew install allure   # Mac
```

## License

This project is for assessment purposes.