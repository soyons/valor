from service.errors.base import BaseServiceError


class AccountNotFound(BaseServiceError):
    pass

class AccountAlreadyRegister(BaseServiceError):
    pass

class AccountRegisterError(BaseServiceError):
    pass

class AccountLoginError(BaseServiceError):
    pass

class InvalidAccountError(BaseServiceError):
    pass