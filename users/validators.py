from django.core.exceptions import ValidationError


def validate_team_member(value):
    user = value.user
    team_board = value.team_board

    if user != team_board.user and user not in (team_board.participants.all() or team_board.admins.all()):
        raise ValidationError('The user must be the creator, an admin, or a participant of the team board.')
