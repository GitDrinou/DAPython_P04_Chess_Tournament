class TournamentError(Exception):
    """Basic exception for tournament related errors."""
    pass


class PlayerRegistrationError(TournamentError):
    """Raised an exception when a player registration fails."""
    pass


class RoundGenerationError(TournamentError):
    """Raised an exception when a round generation fails."""
    pass


class InvalidTournamentStateError(RoundGenerationError):
    """Raised an exception when the state of a tournament to generate a
    round"""
    pass


class InvalidTournamentError(TournamentError):
    """Raised an exception when the selected tournament is invalid."""
    pass


class PlayerDeletionError(TournamentError):
    """Raised an exception when a player deletion fails."""
    pass
