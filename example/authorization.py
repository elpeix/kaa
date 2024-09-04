from kaa import Authorization, Request


class Auth(Authorization):
    def authorize(self, request: Request):
        if request.get_header("AUTHORIZATION") == "token":
            return True
        return False
