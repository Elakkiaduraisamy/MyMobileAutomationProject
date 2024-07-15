Feature: Browser testing

  Scenario: Open a browser and check the title
    Given I open the browser
    When I navigate to "http://example.com"
    Then the title should be "Example Domain"
