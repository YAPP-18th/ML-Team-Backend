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


class NoSuchElementException(Exception):
    def __init__(self, message):
        self.message = message


    def __str__(self):
        return self.message


class InvalidArgumentException(Exception):
    def __init__(self, message):
        self.message = message


    def __str__(self):
        return self.message


    def get_response(self):
        return create_detail(
            param   = self.param,
            field   = self.field,
            message = self.message,
            error   = self.error
        )        