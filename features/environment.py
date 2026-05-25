from unittest.mock import patch, MagicMock

API_BASE_URL = "https://rickandmortyapi.com/api"


MOCK_CHARACTER_RESPONSE = {
    "id": 1,
    "name": "Rick Sanchez",
    "status": "Alive",
    "species": "Human",
    "type": "",
    "gender": "Male",
    "origin": {"name": "Earth (C-137)"},
    "location": {"name": "Citadel of Ricks"},
    "episode": [
        "https://rickandmortyapi.com/api/episode/1",
        "https://rickandmortyapi.com/api/episode/2",
        "https://rickandmortyapi.com/api/episode/3",
        "https://rickandmortyapi.com/api/episode/4",
        "https://rickandmortyapi.com/api/episode/5",
        "https://rickandmortyapi.com/api/episode/6",
    ]
}


def mock_character_get(url, **kwargs):
    mock = MagicMock()
    if url == f"{API_BASE_URL}/character/1":
        mock.status_code = 200
        mock.json.return_value = MOCK_CHARACTER_RESPONSE
    else:
        mock.status_code = 404
        mock.json.return_value = {"error": "Character not found"}
    return mock


def before_scenario(context, scenario):
    print(f"Starting scenario: {scenario.name}")

    if "regression" in scenario.tags:
        context.mock_get = patch("requests.get", side_effect=mock_character_get)
        context.mock_get.start()


def after_scenario(context, scenario):
    print( f"Finished scenario: " f"{scenario.name} - Status: {scenario.status}")

    if "regression" in scenario.tags:
        context.mock_get.stop()