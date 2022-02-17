"""
Notifier contains a series of functions to create notifications for every different
type used in the system, without having to add messy code elsewhere

Also will handle sending info to websockets when we get there
"""
from __future__ import annotations
from django.contrib.auth.models import User
from . import models


def _create_notif(user: User, text: str, link: str, type: str):
    """
    Actually does the work of creating a Notification (and sending it down the websockets later)
    Also is where the notification settings are checked, we won't save notifications that the User doesn't want
    """
    # First we ensure that the User is set up to receive the notification type
    try:
        send = user.settings.notifications[type]
    except (AttributeError, models.Settings.DoesNotExist, KeyError):
        send = True

    if not send:
        return

    # If we make it to this point, create the object and then push updates down the web socket
    models.Notification.objects.create(user=user, text=text, link=link, type=type)
    # TODO - Websocket stuff


def loot_tracker_update(bis: models.BISList, team: models.Team):
    char = bis.owner
    text = f'"{char}"\'s {bis.job.id} BIS List was updated via "{team.name}"\'s Loot Tracker!'
    link = f'/characters/{char.id}/bis_list/{bis.id}/'
    user = char.user
    _create_notif(user, text, link, 'loot_tracker_update')


def team_disband(team: models.Team):
    text = f'"{team.name}" has been disbanded!'
    link = '/'
    # Send to all users that aren't the team leader
    for member in team.members.filter(lead=False):
        _create_notif(member.character.user, text, link, 'team_disband')


def team_join(char: models.Character, team: models.Team):
    text = f'{char} has joined {team.name}!'
    link = f'/team/{team.id}/'
    user = team.members.get(lead=True).character.user
    _create_notif(user, text, link, 'team_join')


def team_kick(member: models.TeamMember):
    char = member.character
    team = member.team
    text = f'{char} has been kicked from {team.name}!'
    link = '/'
    user = char.user
    _create_notif(user, text, link, 'team_kick')


def team_lead(char: models.Character, team: models.Team):
    text = f'{char} has been made the Team Leader of {team.name}!'
    link = f'/team/{team.id}/'
    user = char.user
    _create_notif(user, text, link, 'team_lead')


def team_leave(member: models.TeamMember):
    char = member.character
    team = member.team
    text = f'{char} has left {team.name}!'
    link = f'/team/{team.id}/'
    user = team.members.get(lead=True).character.user
    _create_notif(user, text, link, 'team_leave')


def verify_fail(char: models.Character, error: str):
    text = f'The verification of {char} has failed! Reason: {error}'
    link = f'/characters/{char.id}/'
    user = char.user
    _create_notif(user, text, link, 'verify_fail')


def verify_success(char: models.Character):
    text = f'The verification of {char} has succeeded!'
    link = f'/characters/{char.id}/'
    user = char.user
    _create_notif(user, text, link, 'verify_success')
