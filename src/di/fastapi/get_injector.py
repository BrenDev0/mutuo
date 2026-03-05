from fastapi import Request

def get_injector(
    request: Request
):
    return request.app.state.injector