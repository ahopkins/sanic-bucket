from sanic import Request


def identify_by_remote_addr(request: Request) -> str:
    ident = request.remote_addr
    if not ident and request.conn_info:
        ident = request.conn_info.client_ip

    # If we could not identify, use request ID to not limit
    # TODO:
    # - wha should fallback be?
    #       - semi-random value to allow
    #       - default constant to disallow
    if not ident:
        ident = str(request.id)
    return ident
