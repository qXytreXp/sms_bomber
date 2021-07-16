from src.bomber.services import Service
from ast import literal_eval  # For convert str to dict


def paste_phone_number_to_json(service: Service, phone_number: str) -> None:
    if service.json:
        json = str(service.json)
        service.json = literal_eval(
            json % phone_number
        ) if '%s' in json else literal_eval(json)
    if service.params:
        params = str(service.params)
        service.params = literal_eval(
            params % phone_number
        ) if '%s' in params else literal_eval(params)
    if service.data:
        data = str(service.data)
        service.data = literal_eval(
            data % phone_number) if '%s' in data else literal_eval(data)
