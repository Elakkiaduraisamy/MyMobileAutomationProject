Feature: Product Page Verification
  As a user i am looking to login and select a product frm listed.

  Scenario: standard user logs in
    Given the app is set up
    When the user logs in with standard credentials

  Scenario: Added product to cart
    Given  user selects any products from the list
    Then  user navigates to that product page
    And  Verify the selected product page is displayed
    And  click the add to cart button

   Scenario: verifies the copyrights and social media links
      Given  user scrolls down
      Then  user can see the social media links and copyrights
