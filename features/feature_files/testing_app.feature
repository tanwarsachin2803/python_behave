Feature: Testing App

    @android
    Scenario: User login to the app
        Then the user clicks "surely" on "notification_popup_allow_button" on "landing_page"
        Then the user clicks "surely" on "continue_button" on "landing_page"
        Then the user clicks "surely" on "phone_number_field" on "login_page"
        Then the user enters "9998887776" on the keyboard
        Then the user clicks "surely" on "continue_button" on "login_page"
        Then the user enters "123456" using coordinates
        Then the user clicks "maybe" on "skip_button" on "login_page"
        # Then the user clicks "surely" on "verify_otp_button" on "login_page"

