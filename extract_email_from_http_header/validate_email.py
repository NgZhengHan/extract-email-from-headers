import re

# Constants.
# Remember that in Python, the hyphen "-" needs to be escaped too. 
REGULAR_EXPRESSION = r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$" 

# Result codes.
RESULT_UNDEFINED = 0
RESULT_SUCCESS = 1
RESULT_FAILED_VALIDATION = 2
RESULT_EMAIL_DOES_NOT_END_WITH_SPECIFIC_VALUE = 3
RESULT_GIVEN_EMAIL_END_WITH_IS_NOT_STRING = 4

# Remarks.
REMARKS_UNDEFINED = ""
REMARKS_SUCCESS = "Success."
REMARKS_FAILED_VALIDATION = "Email failed the validation checks."
REMARKS_EMAIL_DOES_NOT_END_WITH_SPECIFIED_VALUE = "Email does not end with the specified value."
REMARKS_GIVEN_EMAIL_END_WITH_IS_NOT_STRING = "The given argument to check if the email ends with a suffix is not an instance of a String. Unable to validate."

# Output index.
OUTPUT_INDEX_RESULT = 0
OUTPUT_INDEX_REMARKS = 1

# Check if the email is valid. 
def validate_email(email : str, ends_with : str = None):
    """
    
    """

    # Initialize the return values.
    result = RESULT_UNDEFINED
    remarks = REMARKS_UNDEFINED
    
    # Use regular expression to check. 
    # 
    # Note: 
    # This is a basic check. It does not validate if the email is deliverable, or 
    # any other considerations such as if it is a trash email etc. 
    match = re.match(REGULAR_EXPRESSION, email)
    
    # Check if there is a match.
    if bool(match):

        # Set the result. 
        result = RESULT_SUCCESS
        remarks = REMARKS_SUCCESS

        # The email matches the regular expression.
        # Check if there is a specified suffix to validate. 
        if ends_with is not None: 

            # There is a specified suffix to validate. Check to see if this given 
            # value is a string. 
            if isinstance(ends_with, str): 

                # The specified suffix is a string. Use it to validate the given 
                # email. 
                if bool(email.endswith(ends_with)):

                    # The given email ends with the specified suffix. 
                    result = RESULT_SUCCESS 
                    remarks = REMARKS_SUCCESS

                else:

                    # The given email does not end with the specified suffix. 
                    result = RESULT_EMAIL_DOES_NOT_END_WITH_SPECIFIC_VALUE
                    remarks = REMARKS_EMAIL_DOES_NOT_END_WITH_SPECIFIED_VALUE + " [" + email + "] does not end with [" + ends_with + "]"
            
            else:

                # The given arugment for checking if the email ends with a certain suffix is 
                # itself not an instance of a String. We are unable to use this. 
                result = RESULT_GIVEN_EMAIL_END_WITH_IS_NOT_STRING
                remarks = REMARKS_GIVEN_EMAIL_END_WITH_IS_NOT_STRING

    else: 

        # The email does not match the regular expression. 
        result = RESULT_FAILED_VALIDATION
        remarks = REMARKS_FAILED_VALIDATION

    # Return the result.
    return result, remarks