Feature: Product Page Verification
  As a user i am looking to login and select a product frm listed.

  Background:
    Given the app is set up
    When the user logs in with standard credentials


  Scenario:
    Given  user selects any products from the list
    Then  user navigates to that product page
    And  Verify the selected product page is displayed
    And  click the add to cart button

   Scenario:
    Given  user selects any products from the list
    Then  user navigates to that product page
     Then user scrolls down to see the social media links and copyrights