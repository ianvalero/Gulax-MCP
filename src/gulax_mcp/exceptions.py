class KronosClientError(RuntimeError):
    """Base error raised by the Kronos REST client."""


class KronosTransportError(KronosClientError):
    """Kronos could not be reached reliably."""


class KronosHTTPError(KronosClientError):
    """Kronos returned an unsuccessful HTTP response."""

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code

        super().__init__(
            f"Kronos API returned HTTP {status_code}"
        )


class KronosInvalidResponseError(KronosClientError):
    """Kronos returned data that does not match its expected contract."""