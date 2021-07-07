def get_detail(param: str, field: str, message: str, err: str):
    detail = [
        {
            'loc': [
                f'{param}', # ex. body
                f'{field}'  # ex. title
            ],
            "msg": message, # ex. field required, not found
            "type": f"{err}.missing" # ex. value_error
        }
    ]
    return detail


class InternalException(Exception):
    def __init__(self, message: str):
        self.message = message


    def __str__(self):
        return self.message   


class NoSuchElementException(Exception):
    def __init__(self, message: str):
        self.message = message


    def __str__(self):
        return self.message


class InvalidArgumentException(Exception):
    def __init__(self, message: str):
        self.message = message


    def __str__(self):
        return self.message 


class RequestConflictException(Exception):
    def __init__(self, message: str):
        self.message = message

    
    def __str__(self):
        return self.message


class ForbiddenException(Exception):
    def __init__(self, message: str):
        self.message = message

    
    def __str__(self):
        return self.message


class RequestInvalidException(Exception):
    def __init__(self, message: str):
        self.message = message
    

    def __str__(self):
        return self.message