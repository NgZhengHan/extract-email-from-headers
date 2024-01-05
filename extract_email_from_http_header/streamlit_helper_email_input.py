import streamlit

from .extract_email_from_headers import extract_email_from_headers
from .extract_email_from_headers import EMAIL_HEADER
from .extract_email_from_headers import SUCCESS as EXTRACT_SUCCESS
from .validate_email import validate_email as validate_email_method
from .validate_email import SUCCESS as VALIDATE_SUCCESS

# Constants. 
EMPTY_STRING = ""

# Helper method to include some additional functions such as 
# 1. Keep the existing email value if it already exists.
# 2. Extract email from headers 
# 3. Validate email
def streamlit_helper_email_input(session_state, 
                                 container = None, 
                                 label = EMPTY_STRING, 
                                 value = EMPTY_STRING, 
                                 max_chars = None, 
                                 session_state_key = None, 
                                 type = "default", 
                                 help = None, 
                                 autocomplete = None, 
                                 on_change = None, 
                                 args =None, 
                                 kwargs = None, 
                                 *, 
                                 header_key = EMAIL_HEADER, 
                                 placeholder = None, 
                                 disabled = False, 
                                 label_visibility = "visible", 
                                 set_email_on_failure = None, 
                                 validate_email = True, 
                                 email_ends_with = None):

    # Check if the session state already has a key for the email. We may already have 
    # some value. This could be due to user manually inputting the email.
    if session_state_key in session_state:
         
         # There already is an key-value entry for the given session state key in the 
         # given session state. We will just use this. 
        pass

    else:
         
        # Extract the email from the header. 
        results_extract_email_from_headers = extract_email_from_headers(session_state, header_key = header_key, session_state_key = session_state_key, set_email_on_failure = set_email_on_failure)
        if results_extract_email_from_headers[0] is EXTRACT_SUCCESS: 
            
            # Check if we should validate the email. 
            if validate_email:
                
                # Validate the email.
                result_validate_email = validate_email_method(session_state[session_state_key], ends_with = email_ends_with)
                if result_validate_email[0] is not VALIDATE_SUCCESS:

                        # Email validation failed. Set the default value. 
                        session_state[session_state_key] = set_email_on_failure

    # Set the value for the text_input if it exists, or a default empty string. 
    # No need to set the value. Value default is an empty string. If there is a 
    # value to the email key, then streamlit will use the key. 
    # Setting both a non-empty string to the value and specifying a key will cause 
    # streamlit to display a warning on the browser page that a value is set while 
    # there is also a session key. 
    #value = session_state.get(key, "")

    # Invoke the Streamlit method using the given parameters. 
    # Remember that a container is optional, so we have to check 
    # for this. 
    if container is not None:

        # There is a container.
        text_input = container.text_input(label = label, 
                                          value = value, 
                                          max_chars = max_chars, 
                                          key = session_state_key, 
                                          type = type, 
                                          help = help, 
                                          autocomplete = autocomplete, 
                                          on_change = on_change, 
                                          args = args, 
                                          kwargs = kwargs, 
                                          placeholder = placeholder, 
                                          disabled = disabled, 
                                          label_visibility = label_visibility)

    else: 
        
        # There is no container. 
        text_input = streamlit.text_input(label = label, 
                                          value = value, 
                                          max_chars = max_chars, 
                                          key = session_state_key, 
                                          type = type, 
                                          help = help, 
                                          autocomplete = autocomplete, 
                                          on_change = on_change, 
                                          args = args, 
                                          kwargs = kwargs, 
                                          placeholder = placeholder, 
                                          disabled = disabled, 
                                          label_visibility = label_visibility)
        
    # Return the result.
    return text_input