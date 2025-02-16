class ExternalAPIError(Exception):
    """Custom exception for external API failures."""
    def __init__(self, endpoint: str, message: str, status_code: int):
        super().__init__(message)
        self.endpoint = endpoint
        self.status_code = status_code
