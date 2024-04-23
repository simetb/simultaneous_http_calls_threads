import simultaneus_requests as sr
request = {
    "METHOD": "POST",
    "URL": "test",
    "HEADERS":{
        "test" : "test",
    },
    "BODY": [],
    "PARAMETERS": {
        "test" : "test",
    }, 
}

sr.do_simultaneus_requests([request])