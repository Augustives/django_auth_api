import os

FIXTURES_DIR = "tests/fixtures"

fixture_files = [
    f[:-3] for f in os.listdir(FIXTURES_DIR) if f.endswith(".py") and f != "__init__.py"
]

pytest_plugins = [f"tests.fixtures.{fixture_file}" for fixture_file in fixture_files]
