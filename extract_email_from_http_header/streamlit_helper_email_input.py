import typing
import streamlit

from . import extract_email_from_headers
from . import validate_email

# Constants.
EMPTY_STRING = ""
STRING_UNDEFINED = "undefined"

# Result codes.
RESULT_UNDEFINED = 0
RESULT_SUCCESS = 1
RESULT_FAIL = 2
RESULT_FAIL_VALIDATION_INPUT_IS_NOT_VALID_EMAIL = 3
RESULT_FAIL_VALIDATION_INPUT_DOES_NOT_END_WITH_SPECIFIC_VALUE = 4

# Remarks.
REMARKS_UNDEFINED = ""
REMARKS_SUCCESS = "Success."
REMARKS_FAIL = "Fail."
REMARKS_FAIL_VALIDATION_INPUT_IS_NOT_VALID_EMAIL = "Fail at validation. The given input is not a valid email address."
REMARKS_FAIL_VALIDATION_INPUT_DOES_NOT_END_WITH_SPECIFIC_VALUE = "Fail at validation. The given input does not end with the specified value."

# Output index.
OUTPUT_INDEX_RESULT = 0
OUTPUT_INDEX_REMARKS = 1
OUTPUT_INDEX_EMAIL = 2


def streamlit_helper_email_input(session_state=streamlit.session_state,
                                 container: streamlit.container = None,
                                 label: str = EMPTY_STRING,
                                 value: str = EMPTY_STRING,
                                 max_chars: int | None = None,
                                 session_state_key: str | int | None = None,
                                 session_state_key_function_output: str | None = None,
                                 type: typing.Literal['default',
                                                      'password'] = "default",
                                 help: str | None = None,
                                 autocomplete: str | None = None,
                                 on_change=None,
                                 args=None,
                                 kwargs=None,
                                 *,
                                 placeholder: str | None = None,
                                 disabled: bool = False,
                                 label_visibility: typing.Literal["visible",
                                                                  "hidden", "collapsed"] = "visible",
                                 header_key: str = extract_email_from_headers.EMAIL_HEADER,
                                 set_email_on_failure: str | None = None,
                                 should_validate_email: bool = True,
                                 email_ends_with: str | None = None) -> str | None:
    """A wrapper function that enhances the Streamlit.text_input function. 

    Optional functions invoked inside this wrapper function is 
        1. validate email
        2. check if email ends with the specified suffix 

    Parameters
    ----------
    Args:
        session_state (SessionStateProxy): 
            Streamlit's session state. Defaults to streamlit.session_state.
            container (streamlit.container, optional): The streamlit container to insert the component into. 
            If value is None, then this will insert the component into wherever it this function is invoked. 
            Defaults to None.
        label (str, optional): 
            A short label explaining to the user what this input is for.
            The label can optionally contain Markdown and supports the following
            elements: Bold, Italics, Strikethroughs, Inline Code, Emojis, and Links.

            This also supports:

            * Emoji shortcodes, such as ``:+1:``  and ``:sunglasses:``.
              For a list of all supported codes,
              see https://share.streamlit.io/streamlit/emoji-shortcodes.

            * LaTeX expressions, by wrapping them in "$" or "$$" (the "$$"
              must be on their own lines). Supported LaTeX functions are listed
              at https://katex.org/docs/supported.html.

            * Colored text, using the syntax ``:color[text to be colored]``,
              where ``color`` needs to be replaced with any of the following
              supported colors: blue, green, orange, red, violet, gray/grey, rainbow.

            Unsupported elements are unwrapped so only their children (text contents) render.
            Display unsupported elements as literal characters by
            backslash-escaping them. E.g. ``1\. Not an ordered list``.

            For accessibility reasons, you should never set an empty label (label="")
            but hide it with label_visibility if needed. In the future, we may disallow
            empty labels by raising an exception.. Defaults to EMPTY_STRING.
        value (str, optional): 
            The text value of this widget when it first renders. This will be
            cast to str internally. If ``None``, will initialize empty and
            return ``None`` until the user provides input. Defaults to empty string. Defaults to EMPTY_STRING.
        max_chars (int | None, optional): 
            Max number of characters allowed in text input. Defaults to None.
        session_state_key (streamlit.Key, optional): 
            An optional string or integer to use as the unique key for the widget.
            If this is omitted, a key will be generated for the widget
            based on its content. Multiple widgets of the same type may
            not share the same key.. Defaults to None.
        session_state_key_function_output (str, optional): 
            An optional string or integer to use as unique key to store the output of this 
            function. Defaults to None.
        type (streamlit.Literal[&#39;default&#39;, &#39;password&#39;], optional): 
            The type of the text input. This can be either "default" (for
            a regular text input), or "password" (for a text input that
            masks the user's typed value). Defaults to "default".. Defaults to "default".
        help (str | None, optional): 
            An optional tooltip that gets displayed next to the input. Defaults to None.
        autocomplete (str | None, optional): 
            An optional value that will be passed to the <input> element's
            autocomplete property. If unspecified, this value will be set to
            "new-password" for "password" inputs, and the empty string for
            "default" inputs. For more details, see https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete. Defaults to None.
        on_change (streamlit.WidgetCallback | None, optional): 
            An optional callback invoked when this text input's value changes. Defaults to None.
        args (streamlit.WidgetArgs | None, optional): 
            An optional tuple of args to pass to the callback. Defaults to None.
        kwargs (streamlit.WidgetKwargs | None, optional): 
            An optional dict of kwargs to pass to the callback. Defaults to None.
        placeholder (str | None, optional): 
            An optional string displayed when the text input is empty. If None,
            no text is displayed. Defaults to None.
        disabled (bool, optional): 
            An optional boolean, which disables the text input if set to True.
            The default is False. Defaults to False.
        label_visibility (streamlit.LabelVisibility, optional): 
            The visibility of the label. If "hidden", the label doesn't show but there
            is still empty space for it above the widget (equivalent to label="").
            If "collapsed", both the label and the space are removed. Default is
            "visible". Defaults to "visible".
        header_key (str, optional): 
            The key in the header of the http requests that is associated with the user's email address. Defaults to EMAIL_HEADER.
        set_email_on_failure (_type_, optional): 
            An optional string to use as the email in the event when the email extraction failes, or when validation fails. Defaults to None.
        should_validate_email (bool, optional): 
            Whether to validate the email. Defaults to True.
        email_ends_with (_type_, optional): 
            Optional string that will be used to check if the email ends with this given string. If None is supplied, then this check will not 
            happen. Defaults to None.

    Returns
    -------
    Returns:
        str | None: The current value of the text input widget or None if no value has been provided by the user.
    """

    # Initialize the return values.
    result = RESULT_UNDEFINED
    remarks = REMARKS_UNDEFINED
    email = STRING_UNDEFINED
    text_input = EMPTY_STRING

    # Check if the session state already has a key for the email. We may already have
    # some value. This could be due to user manually inputting the email.
    if session_state_key in session_state:

        # There already is an key-value entry for the given session state key in the
        # given session state. We will just use this.
        email = session_state[session_state_key]
        pass

    else:

        # There is no entry for the email. We will try to extract it from the http header.

        # Extract the email from the header.
        # 
        # Note: 
        # We set the session_state_key to \"None\" because we do not want the extraction code 
        # to interfere with the session_state key used for the streamlit widget. 
        results_extract_email_from_headers = extract_email_from_headers.extract_email_from_headers(
            session_state, header_key=header_key, session_state_key=None, set_email_on_failure=set_email_on_failure)

        # Check the result of the email extraction.
        if results_extract_email_from_headers[extract_email_from_headers.OUTPUT_INDEX_RESULT] is extract_email_from_headers.RESULT_SUCCESS:

            # Use the extracted email. We will do any validation or checks
            # further down.
            email = results_extract_email_from_headers[extract_email_from_headers.OUTPUT_INDEX_EMAIL]

            # # Successfully extracted email.
            # result = RESULT_SUCCESS

            # # Check if we should validate the email.
            # if validate_email:

            #     # Validate the email.
            #     result_validate_email = validate_email_method(
            #         session_state[session_state_key], ends_with=email_ends_with)
            #     if result_validate_email[0] is not VALIDATE_SUCCESS:

            #         # Email validation failed. Set the default value.
            #         session_state[session_state_key] = set_email_on_failure
        else:

            # Failed to extract email. This means that there has been no prior user input,
            # and that the http header does not contain the email. In this case, we will
            # leave the email as an empty string, so that the placeholder text will be
            # displayed.
            email = EMPTY_STRING
            pass

    # Invoke the Streamlit method using the given parameters.
    # Remember that a container is optional, so we have to check
    # for this.
    if container is not None:

        # There is a container.
        text_input = container.text_input(label=label,
                                          value=email,
                                          max_chars=max_chars,
                                          key=session_state_key,
                                          type=type,
                                          help=help,
                                          autocomplete=autocomplete,
                                          on_change=on_change,
                                          args=args,
                                          kwargs=kwargs,
                                          placeholder=placeholder,
                                          disabled=disabled,
                                          label_visibility=label_visibility)

    else:

        # There is no container.
        text_input = streamlit.text_input(label=label,
                                          value=email,
                                          max_chars=max_chars,
                                          key=session_state_key,
                                          type=type,
                                          help=help,
                                          autocomplete=autocomplete,
                                          on_change=on_change,
                                          args=args,
                                          kwargs=kwargs,
                                          placeholder=placeholder,
                                          disabled=disabled,
                                          label_visibility=label_visibility)

    # Assign the text_input as the email.
    email = text_input

    # We will do validation checks if necessary. We do this here because this is
    # after the point when the user can input their own email.
    if should_validate_email:

        # We should validate the email.
        result_validate_email = validate_email.validate_email(
            email=email, ends_with=email_ends_with)

        # Check the validation result.
        if result_validate_email[validate_email.OUTPUT_INDEX_RESULT] is validate_email.RESULT_SUCCESS:

            # Validation is successful.
            result = RESULT_SUCCESS
            remarks = REMARKS_SUCCESS

        elif result_validate_email[validate_email.OUTPUT_INDEX_RESULT] is validate_email.REMARKS_FAILED_VALIDATION:

            # Validation is not successful.
            result = RESULT_FAIL_VALIDATION_INPUT_IS_NOT_VALID_EMAIL
            remarks = REMARKS_FAIL_VALIDATION_INPUT_IS_NOT_VALID_EMAIL

        elif result_validate_email[validate_email.OUTPUT_INDEX_RESULT] is validate_email.RESULT_EMAIL_DOES_NOT_END_WITH_SPECIFIC_VALUE:

            # Validation is not successful.
            result = RESULT_FAIL_VALIDATION_INPUT_DOES_NOT_END_WITH_SPECIFIC_VALUE
            remarks = REMARKS_FAIL_VALIDATION_INPUT_DOES_NOT_END_WITH_SPECIFIC_VALUE + \
                str(" Input [") + str(email) + str("], specified value for email to end with [") + \
                str(email_ends_with) + str("]")

        else:

            # Generic failure.
            result = RESULT_FAIL
            remarks = REMARKS_FAIL

    else:

        # No need to validate the email.
        pass

    # Associate the output with the non-widget session state key
    if session_state_key_function_output is not None:
        session_state[session_state_key_function_output] = [
            result, remarks, email]

    # Return the result.
    return text_input
