
def minimal_spec(self) -> str:
    """Helper for creating a minimal specification object."""
    _minimal_spec = """
                    openapi: 3.0.3
                    info:
                      title: Swagger Petstore
                      version: 1.0.0
                    paths: {}
                    """
    return _minimal_spec
        