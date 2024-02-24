import streamlit
from streamlit.web.server.websocket_headers import _get_websocket_headers

# Constants.
SESSION_STATE_KEY = "user_email"
EMAIL_HEADER = "X-Email"
EMAIL_UNDEFINED = "undefined"

# Result codes.
RESULT_UNDEFINED = 0
RESULT_SUCCESS = 1
RESULT_FAILURE_UNSPECIFIED = 2
RESULT_NO_EMAIL_HEADER_IN_REQUEST = 3
RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NONE = 4
RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NOT_STRING = 5

# Remarks.
REMARKS_UNDEFINED = ""
REMARKS_SUCCESS = "Success."
REMARKS_FAILURE_UNSPECIFIED = "Unspecified failure."
REMARKS_NO_EMAIL_HEADER_IN_REQUEST = "No email header in the Request."
REMARKS_GIVEN_EMAIL_HEADER_KEY_IS_NONE = "The given email header key to search for is the null object \"None\"."
REMARKS_GIVEN_EMAIL_HEADER_KEY_IS_NOT_STRING = "The given email header key to search for is not a string."
REMARKS_UNABLE_TO_SET_DEFAULT_ON_FAILURE = "Unable to set default email on failure."

# Output index.
OUTPUT_INDEX_RESULT = 0
OUTPUT_INDEX_REMARKS = 1
OUTPUT_INDEX_EMAIL = 2


def extract_email_from_headers(session_state=streamlit.session_state,
                               header_key: str = EMAIL_HEADER,
                               session_state_key: streamlit.Key = SESSION_STATE_KEY,
                               set_email_on_failure: str = None):

    # Initialize the return values.
    email = EMAIL_UNDEFINED
    result = RESULT_UNDEFINED
    remarks = REMARKS_UNDEFINED

    # Get the headers.
    headers = _get_websocket_headers()

    # Validate the given header for email.
    if header_key is None:

        # The given header key to look for is the null value "None". We cannot do anything about
        # this.
        result = RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NONE
        remarks = REMARKS_GIVEN_EMAIL_HEADER_KEY_IS_NONE

    if not isinstance(header_key, str):

        # The given header key to search for is not a string. We cannot proceed.
        result = RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NOT_STRING
        remarks = REMARKS_GIVEN_EMAIL_HEADER_KEY_IS_NOT_STRING

    # Check if we have already failed at this step.
    if result not in {RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NONE, RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NOT_STRING}:

        # Check if there is a header for the email.
        if header_key in headers:

            # Get the value of the email matching the key.
            email = headers.get(header_key)

            # Set the email in the given session state.
            session_state[session_state_key] = email

            # Set the return values.
            result = RESULT_SUCCESS
            remarks = REMARKS_SUCCESS

        else:

            # There is no header for the email.

            # Set the return values.
            result = RESULT_NO_EMAIL_HEADER_IN_REQUEST
            remarks = REMARKS_NO_EMAIL_HEADER_IN_REQUEST
            email = EMAIL_UNDEFINED

    # Additional process if the result is not a success.
    if result in {RESULT_UNDEFINED,
                  RESULT_FAILURE_UNSPECIFIED,
                  RESULT_NO_EMAIL_HEADER_IN_REQUEST,
                  RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NONE,
                  RESULT_GIVEN_EMAIL_HEADER_KEY_IS_NOT_STRING}:

        # Result is not a success.

        # We remove any existing value associated with the given key when this function
        # fails.
        #
        # Note:
        # We use
        #
        # session_state.pop(key, None)
        #
        # here instead of
        #
        # del session_state[key]
        #
        # because it is more elegant. Using del will cause an error if the key does not exist.
        # pop() will remove and return the value if the key exists but we must remember to
        # specify the default value to return ("None" in this example), otherwise it will
        # throw an error.
        session_state.pop(session_state_key, None)

        # Check if we should set an email on failure.
        if set_email_on_failure is not None:

            # Check if the given email to set is a string.
            if isinstance(set_email_on_failure, str):

                # The given email is a string. We can set that.
                email = set_email_on_failure
                session_state[session_state_key] = email

            else:

                # The given email is not a string. We do not set that.
                remarks = remarks + " " + REMARKS_UNABLE_TO_SET_DEFAULT_ON_FAILURE

    # Return the result.
    return result, remarks, email
