import requests
import concurrent.futures
import validates as validate
import message_format as msf

OUTPUT_DATA_LIST: list = []

def do_simultaneus_requests(
    requests_list: list,
    threads_amount: int = 0,
    callback: callable = None,
    dev_status_messages: bool = True
    ):
    
    # Validating the request structure
    for index in range(len(requests_list)):
        validate.check_request_structure(request=requests_list[index])
        requests_list[index]["request_id"] = index + 1
    
    # Validating the thread amount
    validate.check_thread_amount(threads_amount)
    
    if threads_amount == 0:
        threads_amount = len(requests_list)
        
        
    # Saving the callback function to be executed in the threads
    global callback_request 
    callback_request = callback
    
    # Saving the config to know if show the confirm message
    global status_messages
    status_messages = dev_status_messages 
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_amount) as executor:
        executor.map(do_requets, requests_list)
    
    return OUTPUT_DATA_LIST
        
        

def do_requets(request):
    try:

        if request["METHOD"] == "POST" or request["METHOD"] == "PUT":
            response = requests.post(
                url=request["URL"],
                headers=request["HEADERS"],
                json=request["BODY"],
            )
        else:
            response = requests.get(
                url=request["URL"],
                headers=request["HEADERS"],
                data=request["PARAMETERS"],
            )
            
        if response.status_code == 200:
            try:
                if callback_request is not None:
                    do_somethin_request= callback_request(response)
                    if(do_somethin_request is not None): OUTPUT_DATA_LIST.append(do_somethin_request) 
                    else: OUTPUT_DATA_LIST.append(response)
                else: OUTPUT_DATA_LIST.append(response)
                
                print (f'{request["request_id"]} - OK') if status_messages else None
            except:
                raise msf.SimultaneusRequestError(
                    msf.error_message(
                        "004",
                        "DO_SOMETHING_ERROR",
                        "a"
                        "The callback function was not executed for requerst {}, returning None".format(request["request_id"]),
                    )
                )
        else:
            OUTPUT_DATA_LIST.append(None)
            print (f'{request["request_id"]} - ERROR') if status_messages else None
        
    except Exception as exc:
        raise msf.SimultaneusRequestError(
            msf.error_message(
                "003",
                "REQUEST_ERROR",
                "The request {} was not executed: {}".format(request["request_id"],exc),
            )
        )

