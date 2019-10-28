Feature: submit Journal De Bord form

  Scenario: A JDB PSH form can successfully be submitted to the server using simple POST
    Given an instance of the server application
    And a mock db interface
    And valid jdb psh data
      When I submit a complete jdb psh by POST in JSON format
        Then I can check the information has been received

  Scenario: A JDB Entreprise form can successfully be submitted to the server using simple POST
    Given an instance of the server application
    And a mock db interface
    And valid jdb entreprise data
      When I submit a complete jdb entreprise by POST in JSON format
        Then I can check the information has been received
