
Feature: Google Search Test

  Scenario: Test Google Search
    Given I'm on Google search page
    And I type in the text field to search
    When I click the search button
    Then I should be on on the results page