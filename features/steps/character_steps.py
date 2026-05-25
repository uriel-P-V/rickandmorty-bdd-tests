from behave import given, when, then
import requests

API_BASE_URL = "https://rickandmortyapi.com/api"

@given("the rickandmorty API is available")
def step_given_api_available(context):
    response=requests.get(f"{API_BASE_URL}/character/1")
    assert (response.status_code == 200), "API is not available"
    

@when("I request the character with ID {character_id:d}")
def step_when_request_character(context, character_id):
    context.response=requests.get(f"{API_BASE_URL}/character/{character_id}")

@then("the response status code should be {expected_status:d}")
def step_then_status_code(context, expected_status):
    assert ( context.response.status_code == expected_status), (f"Expected status code {expected_status}, "
    f"but got {context.response.status_code}" )

@then("the basic fields should match:")
def step_then_basic_fields(context):

    data = context.response.json()

    for row in context.table:
        field = row["field"]
        expected = row["value"]
        actual_value = data.get(field)

        assert ( str(actual_value) == str(expected)), (
            f"Error in field '{field}': "
            f"expected '{expected}' "
            f"but got '{actual_value}'"
        )

@then("the location and origin should match:")
def step_then_nested_fields(context):

    data = context.response.json()

    for row in context.table:

        field = row["field"]
        expected = row["value"]
        parts = field.split(".")
        actual_value = data[parts[0]][parts[1]]

        assert ( actual_value == expected ), (
            f"Expected {field} to be "
            f"'{expected}', "
            f"but got '{actual_value}'"
        )

@then("the character should have appeared in more than 5 episodes")
def step_then_episodes(context):

    data = context.response.json()

    assert ( len(data["episode"]) > 5), "Character appeared in less than 5 episodes"

@then('the response should contain the error "{expected_error}"')
def step_then_error_message(context, expected_error):

    data = context.response.json()

    assert ( data["error"] == expected_error), (
        f"Expected error '{expected_error}', "
        f"but got '{data['error']}'"
    )