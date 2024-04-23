import requests
import concurrent.futures
import validates as validate
import message_format as msf

DO_SOMETHING: callable = None
OUTPUT_DATA_LIST: list = []

def do_simultaneus_requests(
    requests_list: list,
    threads_amount: int = 0,
    do_something: callable = None,
    ):
    
    # Validating the request structure
    for index in range(len(requests_list)):
        validate.check_request_structure(request=requests_list[index])
        requests_list[index]["request_id"] = index + 1
    
    # Validating the thread amount
    validate.check_thread_amount(threads_amount)
    
    if threads_amount == 0:
        threads_amount = len(requests_list)
        
        
    # Saving the do_something function to be executed in the threads
    DO_SOMETHING = do_something
        
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
                if DO_SOMETHING is not None:
                    do_somethin_request= DO_SOMETHING(response)
                    if(do_somethin_request is not None): OUTPUT_DATA_LIST.append(do_somethin_request) 
                    else: OUTPUT_DATA_LIST.append(response)
                else: OUTPUT_DATA_LIST.append(response)
                print (f'{request["request_id"]} - OK')
            except:
                raise msf.SimultaneusRequestError(
                    msf.error_message(
                        "004",
                        "DO_SOMETHING_ERROR",
                        f"The do_something function was not executed for requerst {request["request_id"]}, returning None",
                    )
                )
        else:
            OUTPUT_DATA_LIST.append(None)
            print (f'{request["request_id"]} - ERROR')
        
    except Exception as exc:
        raise msf.SimultaneusRequestError(
            msf.error_message(
                "003",
                "REQUEST_ERROR",
                f"The request {request["request_id"]} was not executed: {exc}",
            )
        )

