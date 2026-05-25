# rickandmorty-bdd-tests

![CI](https://github.com/uriel-P-V/rickandmorty-bdd-tests/actions/workflows/tests.yml/badge.svg)

A BDD-based test suite for the Rick and Morty API —
demonstrates deep contract validation with Behave and Gherkin,
testing nested JSON structures, list validation,
and mock-based regression testing with a single patch.

---

## Project Structure

```
rickandmorty-bdd-tests/
├── .github/
│   └── workflows/
│       └── tests.yml              ← GitHub Actions CI
├── features/
│   ├── steps/
│   │   └── character_steps.py     ← All step definitions
│   ├── environment.py             ← Hooks and mock setup
│   └── character.feature          ← 5 deep BDD scenarios
└── requirements.txt
```

---

## Features

- **Deep contract validation** — validates basic fields, nested objects and lists
- **Nested field validation** — dynamic dot-notation access (`origin.name`, `location.name`)
- **Episode count validation** — verifies character appearance count from list
- **Error contract testing** — validates error message on 404 responses
- **Single mock** — one `patch("requests.get")` with URL discrimination
- **Tag-driven execution** — `@smoke` hits real API, `@regression` fully mocked
- **GitHub Actions CI** — smoke runs first, regression only if smoke passes

---

## BDD Scenarios

```gherkin
Feature: Rick and Morty Character API

  Background:
    Given the rickandmorty API is available

  @smoke
  Scenario: Get Rick Sanchez
    When I request the character with ID 1
    Then the response status code should be 200

  @regression
  Scenario: Validate basic fields with table
    When I request the character with ID 1
    Then the basic fields should match:
      | field   | value        |
      | id      | 1            |
      | name    | Rick Sanchez |
      | status  | Alive        |
      | species | Human        |
      | gender  | Male         |

  @regression
  Scenario: Validate nested fields: origin and location
    When I request the character with ID 1
    Then the location and origin should match:
      | field         | value            |
      | origin.name   | Earth (C-137)    |
      | location.name | Citadel of Ricks |

  @regression
  Scenario: Validate that it appeared in more than 5 episodes
    When I request the character with ID 1
    Then the character should have appeared in more than 5 episodes

  @regression
  Scenario: Validate an invalid person
    When I request the character with ID 99999
    Then the response status code should be 404
    And the response should contain the error "Character not found"
```

---

## Mock Strategy

Single `patch("requests.get")` with URL discrimination —
returns Rick Sanchez mock data for valid requests, 404 with error message for anything else.

```python
def mock_character_get(url, **kwargs):
    mock = MagicMock()
    if url == f"{API_BASE_URL}/character/1":
        mock.status_code = 200
        mock.json.return_value = MOCK_CHARACTER_RESPONSE
    else:
        mock.status_code = 404
        mock.json.return_value = {"error": "Character not found"}
    return mock
```

---

## Setup

```bash
git clone https://github.com/uriel-P-V/rickandmorty-bdd-tests.git
cd rickandmorty-bdd-tests
pip install -r requirements.txt
behave
```

---

## Running Tests

```bash
# All scenarios
behave

# Smoke only — hits real Rick and Morty API
behave --tags=smoke

# Regression only — fully mocked, no internet required
behave --tags=regression
```

---

## CI/CD Pipeline

Two dependent jobs run on every push and pull request to `main`:

```
push / PR → smoke (1 scenario) → regression (4 scenarios)
```

If `smoke` fails, `regression` is skipped automatically.

---

## Tech Stack

- **Python 3.11+**
- **Behave** — BDD framework with Gherkin support
- **Requests** — HTTP client for API calls
- **unittest.mock** — patch, MagicMock, side_effect
- **GitHub Actions** — CI/CD pipeline

---

## Author

**Uriel Alejandro Pérez Valdovinos**  
[github.com/uriel-P-V](https://github.com/uriel-P-V) · [linkedin.com/in/uriel-pv](https://linkedin.com/in/uriel-pv)