Feature: Home Page interactions

  Scenario: Verify search functionality
    Given the app is installed
    When I click on the search button
    Then I should see the search bar
    And I navigate back to the main page
    And I should see the UI catalog
    When I swipe up
    And I swipe down
    And I scroll to the webview element
    Then I should switch to the webview context
    And I switch back to the native context
    When I swipe right
    And I swipe left
