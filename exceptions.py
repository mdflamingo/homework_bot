class StatusCodeError(Exception):
    """Использутся при статусе кода отлтчном от HTTPStatus.OK."""

    pass


class APIRequestError(Exception):
    """Запрос не доходит до API."""

    pass


class JsonError(Exception):
    """Объект не преобразовался из json."""

    pass
