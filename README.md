# simultaneus_requests: Python Library for Concurrent Requests

This Python library, simultaneus_requests (sic), enables you to execute multiple HTTP requests concurrently using threads. It supports various request methods (GET, POST, PUT, DELETE) and provides options for customizing thread count and handling responses.

```bash
pip install requests concurrent.futures
```
or

```bash
pip install -r requirements.txt
```

## Key Features
- Concurrent Requests: Send multiple HTTP requests simultaneously to improve performance.
- Supported Methods: Handle GET, POST, PUT, and DELETE requests.
- Thread Management: Specify the number of threads to use for execution.
- Response Handling:
  - Callback Function: Define a callback function to process responses in the threads.
  - Data Access: Access processed data (if a callback is used) or raw responses in the returned list.
- Error Handling:
  - Request Errors: Exceptions are raised for failed requests, providing details.
  - Callback Errors: Exceptions are raised if the callback function encounters issues.
- Optional Status Messages: Control the display of request status messages during execution.

## Usage
1. Import the simultaneus_requests library:
```python
import simultaneus_requests as sr
```

2. Define a list of requests, where each request is a dictionary with the following keys:
- METHOD: The HTTP method (GET, POST, PUT, DELETE).
- URL: The target URL of the request.
- HEADERS (optional): A dictionary of headers to include in the request.
- BODY (optional): The data to send in the request body (for POST and PUT methods).
- PARAMETERS (optional): A dictionary of parameters to append to the URL (for GET requests).
- request_id (optional): An identifier for the request (automatically assigned if not provided).

3. Define a callback function (optional) to process responses in the threads. This function should take a requests.Response object as input and return the processed data.

4. Call the do_simultaneus_requests function with the following arguments:
- requests_list: The list of request dictionaries.
- threads_amount (optional): The number of threads to use (defaults to the number of requests if not specified).
- callback (optional): The callback function for response processing.
- dev_status_messages (optional): A boolean flag to enable or disable status messages during execution (defaults to True).

5. The function returns a list containing the processed data from the callback function (if used) or the raw response objects.

## Example
```python
import simultaneus_requests as sr

request = {
    "METHOD": "GET",
    "URL": "https://reqres.in/api/users",
    "PARAMETERS": {
        "page": "1",
    },
}

def do_something(data):
    print(f"Data: {data}")  # Process the data here

data = sr.do_simultaneus_requests(
    [request],
    threads_amount=1,
    callback=do_something,
)

# Access processed data or raw responses from the returned list (data)
```
## Error Handling
The do_simultaneus_requests function raises exceptions for errors during request execution or callback processing. These exceptions provide details for troubleshooting.

## Additional Notes
- For advanced usage, you can customize the error handling behavior by subclassing the SimultaneusRequestError exception.
- Consider using environment variables or a configuration file to manage settings like thread count.

## Future Enhancements
- Support for asynchronous requests using libraries like asyncio.
- Integration with logging frameworks for more detailed logging capabilities.
- Timeout options for individual requests.
