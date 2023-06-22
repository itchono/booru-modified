from aiohttp import ClientSession

class ClientSessionMixin:
    http_session: ClientSession