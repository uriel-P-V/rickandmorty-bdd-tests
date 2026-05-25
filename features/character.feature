Feature:Rick and Morty Character API

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
            |field    | value        |
            |id       | 1            |
            |name     | Rick Sanchez |
            |status   | Alive        |
            |species  | Human        |
            |gender   | Male         |

    @regression
    Scenario: Validate nested fields: origin and location
        When I request the character with ID 1
        Then the location and origin should match:
            | field           | value              |
            | origin.name     | Earth (C-137)      |
            | location.name   | Citadel of Ricks   |
         

    @regression
    Scenario: Validate that it appeared in more than 5 episodes
        When I request the character with ID 1
        Then the character should have appeared in more than 5 episodes
    

    @regression
    Scenario: Validate an invalid person
        When I request the character with ID 99999
        Then the response status code should be 404
        And the response should contain the error "Character not found"
