Feature: Landing Page
    Background: 
        Given the user opens the website
        Given the user switches to iframe "frame_locator" on "landing_page"
        Then the user waits for 1 seconds

    @website
    Scenario: User can open the website
        Then the user verifies "login_link" is "visible" on "landing_page"
        Then the user clicks pageobject on "login_link" on "landing_page"


