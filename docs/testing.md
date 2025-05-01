# Testing

This guide explains how to run tests for the Personalized Learning Path Generator API.

## Test Structure

Tests are organized into the following files:

- `conftest.py` - Contains fixtures and test configuration
- `test_auth.py` - Tests for authentication endpoints
- `test_courses.py` - Tests for course management endpoints
- `test_learning_paths.py` - Tests for learning path endpoints

## Running Tests

To run all tests:

```bash
pytest tests/
```

To run a specific test file:

```bash
pytest tests/test_auth.py
```

To run tests with verbose output:

```bash
pytest -v tests/
```

## Test Coverage

To measure test coverage, install pytest-cov:

```bash
pip install pytest-cov
```

Then run:

```bash
pytest --cov=. tests/
```

This will show the coverage report, indicating how much of your code is being tested.

## Writing New Tests

When adding new features to the API, make sure to add corresponding test cases following these guidelines:

1. Use fixtures from `conftest.py` when possible
2. Test both successful and error cases
3. Verify that authentication is properly enforced on protected endpoints
4. Include tests for edge cases specific to your feature