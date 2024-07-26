Feature: App flow testing

  Scenario: Standard user login
    Given the app is set up
    When the user logs in with standard credentials
    Then the user should be logged in successfully

  Scenario: user log out
    Given user is logged in
    When the user clicks log out
    Then user logs out and login page is shown


Scenario: Wrong user login
 Given the app is set up
 When the user logs in with wrong user credentials
 Then the user should able to see error message
