Feature: App flow testing

  Scenario: Standard user login
    Given the app is set up
    When the user logs in with standard credentials
    Then the user should be logged in successfully

   Scenario: Standard user login
    Given the app is set up
    When the user logs in with wronguser credentials
    Then the user should able to see error message
