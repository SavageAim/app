"""
Model for managing the Teams in the system
"""
# stdlib
import string
import uuid
from random import choice
# lib
from django.db import models
# local
from api import notifier
from .character import Character

CHARS = string.ascii_letters + string.digits
CODE_LEN = 32


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invite_code = models.CharField(max_length=CODE_LEN)
    name = models.CharField(max_length=64)
    # job_id: overridden_position
    solver_sort_overrides = models.JSONField(default=dict)
    tier = models.ForeignKey('Tier', on_delete=models.CASCADE)

    def __str__(self):
        return f'Team {self.name} @ {self.tier.name}'

    def disband(self):
        """
        Disband the Team.
        Assumes this method is called by someone with authority.
        """
        # Send notification and then delete the object I guess
        notifier.team_disband(self)

        # Clean up any proxy characters
        for tm in self.members.filter(character__user__isnull=True):
            char = tm.character
            tm.delete()
            char.delete()

        # Wipe the Team from the DB
        self.delete()

    @staticmethod
    def generate_invite_code() -> str:
        """
        Generate a new invite code for a team
        Can be used to regenerate the code later as needed
        """
        code = ''.join(choice(CHARS) for _ in range(CODE_LEN))
        while Team.objects.filter(invite_code=code).exists():
            code = ''.join(choice(CHARS) for _ in range(CODE_LEN))

        return code

    def make_lead(self, new_lead: Character):
        """
        Make the specified Character the leader of the Team.
        Does nothing if the specified Character is the current leader.
        """
        curr_lead = self.members.get(lead=True)
        if curr_lead.id == new_lead.id:  # pragma: no cover
            # Make sure we have to do this before we run any code (don't do any unnecessary database hits)
            return

        curr_lead.lead = False
        curr_lead.save()
        new_lead.lead = True
        new_lead.permissions = 0
        new_lead.save()
        notifier.team_lead(new_lead.character, self)

    def remove_character(self, char: Character, kick: bool):
        """
        Remove a character from the Team. This comes with some clauses;
            - Firstly, we assume this is called by someone with permission.
            - If they are the only non-proxy character, we disband the team instead
            - If they are the leader, we pass leader to someone else, including sending the notification
            - Finally, remove the character and send notification
        """
        if self.members.count() == 1:
            self.disband()
            return

        char_member = self.members.get(character=char)
        if char_member.lead:
            # Find the first non-proxy non-leader Member in the Team
            new_lead = self.members.filter(lead=False, character__user__isnull=False).distinct().first()

            # If new_lead is None then there are no more non proxy non leader members
            # That means the team is empty, so disband
            if new_lead is None:
                self.disband()
                return

            # If not, make them the new leader
            self.make_lead(new_lead)

        if kick:
            notifier.team_kick(char_member)
        else:
            notifier.team_leave(char_member)
        char_member.delete()
