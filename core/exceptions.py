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


class RoundError(TournamentError):
    """Basic exception for round related errors."""
    pass


class RoundStartError(RoundError):
    """Raised an exception when a round start fails."""
    pass


class RoundEndError(RoundError):
    """Raised an exception when a round end fails."""
    pass


class MatchScoreError(RoundError):
    """Raised an exception when scores saving fails."""

    def __init__(self, message, match_id=None):
        super().__init__(message)
        self.match_id = match_id

    def __str__(self):
        if self.match_id:
            return f"{super().__str__()} (ID du match : {self.match_id})"
        return super().__str__()


class ReportError(TournamentError):
    """Basic exception for report related errors."""
    pass


class NoPlayersError(ReportError):
    """Raised an exception when no players are registered."""
    pass


class NoTournamentsError(ReportError):
    """Raised an exception when no tournaments are registered."""
    pass


class InvalidTournamentsSelectionError(ReportError):
    """Raised an exception when a tournament selection fails."""
    pass
