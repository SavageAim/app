# stdlib
from datetime import timedelta
from io import StringIO
from typing import Dict
from unittest.mock import patch
# lib
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.core.management import call_command
from django.utils import timezone
# local
from api.lodestone_scraper import LodestoneScraper
from api.models import BISList, Character, Gear, Job, Notification, Team, Tier
from api.tasks import cleanup, verify_character, remind_users_to_verify
from .test_base import SavageAimTestCase


# Pretend to be a logger
LOGGER = type('logger', (), {'error': lambda msg: msg})


# Mock response functions
def get_desktop_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for the desktop site
    """
    char_id = url.split('/')[-1]
    obj = Character.objects.filter(lodestone_id=char_id).first()
    body = f'<html><head></head><body><div class="character__selfintroduction">{obj.token}</div></body></html>'
    return type('response', (), {'status_code': 200, 'content': body})


def get_mobile_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for the mobile site
    """
    char_id = url.split('/')[-1]
    obj = Character.objects.filter(lodestone_id=char_id).first()
    body = f'<html><head></head><body><div class="character__character_profile">{obj.token}</div></body></html>'
    return type('response', (), {'status_code': 200, 'content': body})


def get_empty_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for a site that doesn't contain the token we need
    """
    body = '<html><head></head><body><div class="character__character_profile"></div></body></html>'
    return type('response', (), {'status_code': 200, 'content': body})


def get_error_response(url: str, headers: Dict[str, str]):
    """
    Return a faked http response object for a non 200 error
    """
    return type('response', (), {'status_code': 400, 'content': 'Invalid request.'})


def get_token_response(url: str, data: Dict[str, str]):
    """
    Return a faked http response for a valid refresh token
    """
    return type(
        'response',
        (),
        {
            'status_code': 200,
            'json': lambda: {
                'access_token': 'new access token',
                'refresh_token': 'new refresh token',
                'expires_in': 60 * 60 * 24,
            },
        },
    )


class TasksTestSuite(SavageAimTestCase):
    """
    Test the functions in the tasks file to make sure they work as intended

    Mock requests to return pre-determined html bodies
    """

    def setUp(self):
        # Call LodestoneScraper.get_instance here so it's unaffected by mocks
        LodestoneScraper.get_instance()

    def tearDown(self):
        Notification.objects.all().delete()
        Team.objects.all().delete()
        BISList.objects.all().delete()
        Character.objects.all().delete()

    def test_cleanup(self):
        """
        - Test the cleanup task by creating a couple of different Characters and running the task
        - Then ensure that the ones that should have been deleted are erased from the DB
        - Ensure that Proxies aren't deleted
        """
        old_unver = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
        )
        # Give them a BISList and a Team
        g = Gear.objects.create(name='Test', item_level=600, has_weapon=True, has_armour=True, has_accessories=True)
        bis = BISList.objects.create(
            bis_body=g,
            bis_bracelet=g,
            bis_earrings=g,
            bis_feet=g,
            bis_hands=g,
            bis_head=g,
            bis_left_ring=g,
            bis_legs=g,
            bis_mainhand=g,
            bis_necklace=g,
            bis_offhand=g,
            bis_right_ring=g,
            current_body=g,
            current_bracelet=g,
            current_earrings=g,
            current_feet=g,
            current_hands=g,
            current_head=g,
            current_left_ring=g,
            current_legs=g,
            current_mainhand=g,
            current_necklace=g,
            current_offhand=g,
            current_right_ring=g,
            job=Job.objects.create(display_name='PLD', id='PLD', name='PLD', ordering=0, role='tank'),
            owner=old_unver,
        )
        team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Test Team 1',
            tier=Tier.objects.create(max_item_level=600, name='Test', raid_gear_name='Test', tome_gear_name='Test'),
        )
        team.members.create(character=old_unver, bis_list=bis, lead=True)
        old_ver = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=11289475,
            user=self._get_user(),
            name='Char 2',
            world='Lich',
            verified=True,
        )
        proxy = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=11289475,
            user=None,
            name='Char 2',
            world='Lich',
            verified=False,
        )
        # Update all created stamps to 2 weeks ago
        Character.objects.update(created=timezone.now() - timedelta(days=14))
        # Create one last character that's new
        new_unver = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=2498174123,
            user=self._get_user(),
            name='Char 3',
            world='Lich',
            verified=False,
        )

        # Run the cleanup task and ensure the DB is as it should be
        cleanup()
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=old_unver.pk)
        self.assertEqual(Character.objects.filter(pk__in=[old_ver.pk, new_unver.pk, proxy.pk]).count(), 3)

        # Check that the BIS and Team were properly deleted
        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(pk=team.pk)
        with self.assertRaises(BISList.DoesNotExist):
            BISList.objects.get(pk=bis.pk)

    @patch('requests.post', side_effect=get_token_response)
    def test_token_refresh(self, mocked_post):
        """
        Test a refresh token attempt while mocking the request
        """
        app = SocialApp.objects.create()
        account = SocialAccount.objects.create(
            user=self._get_user(),
        )
        token = SocialToken.objects.create(
            expires_at=timezone.now() + timedelta(hours=6),
            token='current token',
            token_secret='current secret',
            account_id=account.id,
            app_id=1,
        )

        call_command('refresh_tokens', stdout=StringIO(), stderr=StringIO())
        new_token_data = SocialToken.objects.first()

        self.assertNotEqual(token.token, new_token_data.token)
        self.assertNotEqual(token.token_secret, new_token_data.token_secret)
        self.assertGreater(new_token_data.expires_at, token.expires_at)

        app.delete()

    @patch('requests.get', side_effect=get_desktop_response)
    def test_verify_character(self, mocked_get):
        """
        Test a full verification call for a character is successful

        Also ensure that other copies of this character get deleted
        """
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        other_version = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._create_user(),
            name='Char 2',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        third_version = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=char.user,
            name='Char 3',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        verify_character(char.pk)

        char.refresh_from_db()
        self.assertTrue(char.verified)
        self.assertEqual(Notification.objects.count(), 1)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=third_version.pk)

        # Ensure that the one owned by a different user is still present to be deleted
        Character.objects.get(pk=other_version.pk)

        # Check for Notification
        notif = Notification.objects.first()
        message = f'The verification of {char} has succeeded!'
        self.assertEqual(notif.text, message)

    @patch('requests.get', side_effect=get_desktop_response)
    def test_verify_proxy_assimilation(self, mocked_get):
        """
        Test a full verification call for a character is successful

        Ensure that Proxy Characters get properly assimilated.
        """
        call_command('seed', stdout=StringIO())
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        # Create a Team first
        team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=605),
        )

        # Create a Team lead to use to create a proxy character
        proxy = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=char.lodestone_id,
            user=None,
            name='Team Lead',
            verified=False,
            world='Lich',
        )
        raid_weapon = Gear.objects.get(item_level=605, name='Asphodelos')
        raid_gear = Gear.objects.get(item_level=600, has_weapon=False)
        tome_gear = Gear.objects.get(item_level=600, has_weapon=True)
        crafted = Gear.objects.get(name='Classical')
        bis = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='SGE',
            owner=proxy,
        )

        # Lastly, link the characters to the team
        tm = team.members.create(character=proxy, bis_list=bis, lead=True)

        # Verify, then we check that the Proxy was deleted, and that the existing character is now the only member
        verify_character(char.pk)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=proxy.pk)

        team.refresh_from_db()
        self.assertEqual(team.members.count(), 1)
        tm.refresh_from_db()
        self.assertEqual(tm.character_id, char.id)
        self.assertEqual(tm.bis_list_id, bis.id)
        bis.refresh_from_db()
        self.assertEqual(bis.owner_id, char.id)

    @patch('requests.get', side_effect=get_error_response)
    def test_verify_character_failures(self, mocked_get):
        """
        Handle errors in the verification code to ensure it all works as expected
        """
        # Start with an already verified character
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=True,
            token=Character.generate_token(),
        )
        verify_character(char.pk)
        mocked_get.assert_not_called()

        # Unverify the character and attempt to, then check the notifications for the reason why
        char.verified = False
        char.save()
        verify_character(char.pk)
        mocked_get.assert_called_once()

        # Check for Notification
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        error = 'Lodestone may be down.'
        message = f'The verification of {char} has failed! Reason: {error}'
        self.assertEqual(notif.text, message)

    def test_verify_reminder(self):
        """
        Create a non-verified character that is 6 days old.
        Run the task twice.
        Ensure we get 1 notification about it.
        """
        old_unver = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=1234567890,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
        )
        Character.objects.update(created=timezone.now() - timedelta(days=5))
        # Run the reminder function once, ensure the notification is created
        remind_users_to_verify()
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.link, f'/characters/{old_unver.id}/')
        self.assertEqual(
            notif.text,
            f'"{old_unver}" has not been verified in at least 5 days! In 2 more they will be deleted!',
        )

        # Run the function again, ensure that there is still only one notif
        Character.objects.update(created=timezone.now() - timedelta(days=6))
        remind_users_to_verify()
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().pk, notif.pk)

    @patch('requests.get', side_effect=get_desktop_response)
    @patch('api.notifier.team_proxy_claim')
    def test_verify_bug_where_other_unverified_characters_are_used_for_something(self, *args):
        """
        Test Plan:
            - Replicate the bug from Jan 7th
                - Cannot delete some instances of model 'Character' because they are referenced through protected foreign keys: 'BISList.owner'."
            - Appears to happen as a result of the other unverified characters being owned and being in use as opposed to being proxies
        """
        call_command('seed', stdout=StringIO())
        lodestone_id = '1234567890'
        # in the bug, the proxy was created before the character being verified
        other_owned_character = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=lodestone_id,
            user=self._get_user(),
            name='Char 1',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        # Create a Team first
        team = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=605),
        )
        team2 = Team.objects.create(
            invite_code=Team.generate_invite_code(),
            name='Les Jambons',
            tier=Tier.objects.get(max_item_level=605),
        )

        # Create the Character that we will be verifying
        char = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=lodestone_id,
            user=other_owned_character.user,
            name='Char 2',
            verified=False,
            world='Lich',
        )
        proxy = Character.objects.create(
            avatar_url='https://img.savageaim.com/abcde',
            lodestone_id=lodestone_id,
            user=None,
            name='Char 3',
            world='Lich',
            verified=False,
            token=Character.generate_token(),
        )
        raid_weapon = Gear.objects.get(item_level=605, name='Asphodelos')
        raid_gear = Gear.objects.get(item_level=600, has_weapon=False)
        tome_gear = Gear.objects.get(item_level=600, has_weapon=True)
        crafted = Gear.objects.get(name='Classical')
        bis = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='SGE',
            owner=other_owned_character,
        )
        bis2 = BISList.objects.create(
            bis_body=raid_gear,
            bis_bracelet=raid_gear,
            bis_earrings=raid_gear,
            bis_feet=raid_gear,
            bis_hands=tome_gear,
            bis_head=tome_gear,
            bis_left_ring=tome_gear,
            bis_legs=tome_gear,
            bis_mainhand=raid_weapon,
            bis_necklace=tome_gear,
            bis_offhand=raid_weapon,
            bis_right_ring=raid_gear,
            current_body=crafted,
            current_bracelet=crafted,
            current_earrings=crafted,
            current_feet=crafted,
            current_hands=crafted,
            current_head=crafted,
            current_left_ring=crafted,
            current_legs=crafted,
            current_mainhand=crafted,
            current_necklace=crafted,
            current_offhand=crafted,
            current_right_ring=crafted,
            job_id='PLD',
            owner=proxy,
        )

        # Put the proxy character on the team
        tm = team.members.create(character=other_owned_character, bis_list=bis, lead=True)
        tm2 = team2.members.create(character=proxy, bis_list=bis2, lead=False)

        # Attempt to verify the proxy character, which for some reason is causing a protected error
        self.assertEqual(Character.objects.count(), 3)
        verify_character(char.pk)
        self.assertEqual(Character.objects.count(), 1)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=proxy.pk)
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(pk=other_owned_character.pk)

        tm.refresh_from_db()
        self.assertEqual(tm.character_id, char.pk)
        tm2.refresh_from_db()
        self.assertEqual(tm2.character_id, char.pk)

        bis.refresh_from_db()
        self.assertEqual(bis.owner_id, char.id)
        bis2.refresh_from_db()
        self.assertEqual(bis2.owner_id, char.id)
