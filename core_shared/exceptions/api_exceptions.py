class SpaceTrackError(Exception):
    """Base exception class for all Space-Track API related errors."""
    pass

class AuthenticationError(SpaceTrackError):
    """Raised when login to Space-Track.org fails due to invalid credentials."""
    pass

class RateLimitExceededError(SpaceTrackError):
    """Raised when we exceed the 30 requests/min or 300 requests/hour limit."""
    pass