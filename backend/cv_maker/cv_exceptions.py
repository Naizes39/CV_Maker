class CVException(Exception):
    pass

class ValidationError(CVException):
    pass

class TypeValidationError(CVException):
    pass

class MissingDataError(ValidationError):
    pass

class SectionError(CVException):
    pass

class GenerationError(CVException):
    pass