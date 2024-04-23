import message_format as msf


# Functions to check the thread amount
def check_thread_amount(thread_amount: int) -> None:
    # Check if the thread amount is valid (int)
    if(not isinstance(thread_amount, int)):
        raise msf.SimultaneusRequestError(
            msf.error_message("002",
                              "THREAD_AMOUNT_ERROR",
                              "Thread amount must be an integer"),
        )
        
    # Check if the thread amount is positive (int)
    if(thread_amount < 0):
        msf.SimultaneusRequestError(
            msf.error_message("002",
                              "THREAD_AMOUNT_ERROR",
                              "Thread amount must be positive, but it is negative"),
        )
    
# Function to check the request structure
def check_request_structure(request: dict) -> None:
    basic_keys = ['METHOD', 'URL', "HEADERS"]
    
    # Check the basic structure
    if not all(key in request for key in basic_keys):
        raise msf.SimultaneusRequestError(
            msf.error_message("000",
                            "REQUEST_STRUCTURE_ERROR", 
                            "Request basic structure is not valid"))
    
    # Check if the method is valid
    method_valid_values = ['GET', 'POST', 'PUT', 'DELETE']
    if request['METHOD'] not in method_valid_values:
        raise msf.SimultaneusRequestError(
            msf.error_message("001",
                            "METHOD_NOT_VALID",
                            f"Method '{request['METHOD']}' is not valid"))
    
    # Check if the request method structure is valid
    if request['METHOD'] == 'GET' or request['METHOD'] == 'DELETE':
        _valid_method_request("PARAMETERS",request)
    else:
        _valid_method_request("BODY",request)
    
# Function to check the method request structure
def _valid_method_request(data_transfer, request):
    
    # Check if the data_transfer key is present
    if(data_transfer not in request):
        raise msf.SimultaneusRequestError(
            msf.error_message("000",
                            "REQUEST_STRUCTURE_ERROR", 
                            f"{data_transfer} is missing in request"))
    
    # Check if the data_transfer is valid (dict)
    if(not isinstance(request[data_transfer], dict)):
        raise msf.SimultaneusRequestError(
            msf.error_message("000",
                            "REQUEST_STRUCTURE_ERROR", 
                            f"{data_transfer} is not a dict"))