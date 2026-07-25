class DomainError(Exception):
    """Erro base de regra de negócio."""


class NotFoundError(DomainError):
    pass


class AlreadyExistsError(DomainError):
    pass


class InvalidCredentialsError(DomainError):
    pass
