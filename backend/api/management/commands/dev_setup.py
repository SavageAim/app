from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from api import models


class Command(BaseCommand):
    help = 'Populate the Dev DB with some data that should make it useable by new devs.'

    def handle(self, *args, **options):
        # Firstly, ensure we're using local by attempting to import from admin
        if User.objects.filter(username='devuser').exists():
            response = input('DB appears to already be set up. Would you like to recreate it? [y/N] ')
            if len(response) == 0 or response.lower()[0] != 'y':
                return
            # Wipe the DB and set it all up again
            print('Cleaning up existing objects')
            models.Team.objects.all().delete()
            models.BISList.objects.all().delete()
            models.Character.objects.all().delete()
            User.objects.all().delete()

        print('Creating Users')
        user1 = User.objects.create_superuser(username='devuser', password='password', first_name='Dev User 1')
        user2 = User.objects.create_superuser(username='devuser2', password='password', first_name='Dev User 2')

        print('Creating Characters')
        models.Character.objects.create(
            avatar_url='https://placehold.co/96/2E53A5/F3F3EC.png?text=1',
            lodestone_id='1',
            name='Character 1',
            token=models.Character.generate_token(),
            user=user1,
            world='Dev',
        )
        char2 = models.Character.objects.create(
            avatar_url='https://placehold.co/96/2E53A5/F3F3EC.png?text=2',
            lodestone_id=2,
            name='Character 2',
            token=models.Character.generate_token(),
            user=user1,
            verified=True,
            world='Dev',
        )
        char3 = models.Character.objects.create(
            avatar_url='https://placehold.co/96/2E53A5/F3F3EC.png?text=3',
            lodestone_id='3',
            name='Character 3',
            token=models.Character.generate_token(),
            user=user2,
            verified=True,
            world='Dev',
        )
        char4 = models.Character.objects.create(
            avatar_url='https://placehold.co/96/2E53A5/F3F3EC.png?text=4',
            lodestone_id=4,
            name='Character 4',
            token=models.Character.generate_token(),
            user=None,
            verified=True,
            world='Dev',
        )

        # Get the info for setting up BIS Lists and Teams
        tier = models.Tier.objects.first()
        raid_weapon = models.Gear.objects.get(
            item_level=tier.max_item_level,
            name=tier.raid_gear_name,
            has_weapon=True,
        )
        raid_gear = models.Gear.objects.get(
            item_level=tier.max_item_level - 5,
            name=tier.raid_gear_name,
            has_weapon=False,
        )
        tome_gear = models.Gear.objects.get(
            item_level=tier.max_item_level - 5,
            name=tier.tome_gear_name,
        )
        crafted_gear = models.Gear.objects.get(
            item_level=tier.max_item_level - 25,
            has_weapon=True,
            has_armour=True,
            has_accessories=True,
        )

        current_stuff = {
            f'current_{slot}': crafted_gear
            for slot in ['mainhand', 'offhand', 'head', 'body', 'hands', 'legs', 'feet', 'earrings', 'necklace', 'bracelet', 'right_ring', 'left_ring']
        }

        print('Creating BIS Lists')
        bis21 = models.BISList.objects.create(
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=tome_gear,
            bis_hands=raid_gear,
            bis_legs=tome_gear,
            bis_feet=raid_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=raid_gear,
            bis_left_ring=tome_gear,
            job_id='PLD',
            name='Tonk',
            owner=char2,
            **current_stuff,
        )
        bis22 = models.BISList.objects.create(
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=tome_gear,
            bis_body=raid_gear,
            bis_hands=tome_gear,
            bis_legs=raid_gear,
            bis_feet=tome_gear,
            bis_earrings=raid_gear,
            bis_necklace=tome_gear,
            bis_bracelet=raid_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            job_id='WHM',
            name='Healz',
            owner=char2,
            **current_stuff,
        )
        bis23 = models.BISList.objects.create(
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=raid_gear,
            bis_hands=tome_gear,
            bis_legs=tome_gear,
            bis_feet=raid_gear,
            bis_earrings=raid_gear,
            bis_necklace=raid_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            job_id='DRG',
            name='Deeps',
            owner=char2,
            **current_stuff,
        )
        bis31 = models.BISList.objects.create(
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=tome_gear,
            bis_body=tome_gear,
            bis_hands=raid_gear,
            bis_legs=raid_gear,
            bis_feet=tome_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=raid_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            job_id='WAR',
            name='Tonk',
            owner=char3,
            **current_stuff,
        )
        bis32 = models.BISList.objects.create(
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=raid_gear,
            bis_hands=raid_gear,
            bis_legs=tome_gear,
            bis_feet=tome_gear,
            bis_earrings=tome_gear,
            bis_necklace=raid_gear,
            bis_bracelet=raid_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            job_id='SGE',
            name='Healz',
            owner=char3,
            **current_stuff,
        )
        bis33 = models.BISList.objects.create(
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=tome_gear,
            bis_body=tome_gear,
            bis_hands=tome_gear,
            bis_legs=raid_gear,
            bis_feet=raid_gear,
            bis_earrings=raid_gear,
            bis_necklace=tome_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            job_id='PCT',
            name='Deeps',
            owner=char3,
            **current_stuff,
        )
        bis4 = models.BISList.objects.create(
            bis_mainhand=raid_weapon,
            bis_offhand=raid_weapon,
            bis_head=raid_gear,
            bis_body=tome_gear,
            bis_hands=raid_gear,
            bis_legs=raid_gear,
            bis_feet=raid_gear,
            bis_earrings=tome_gear,
            bis_necklace=tome_gear,
            bis_bracelet=tome_gear,
            bis_right_ring=tome_gear,
            bis_left_ring=raid_gear,
            job_id='MCH',
            name='Deeps',
            owner=char4,
            **current_stuff,
        )

        print('Creating Teams')
        team1 = models.Team.objects.create(
            invite_code=models.Team.generate_invite_code(),
            name='Team 1',
            tier=tier,
        )
        models.TeamMember.objects.create(
            bis_list=bis21,
            character=char2,
            lead=True,
            team=team1,
        )
        models.TeamMember.objects.create(
            bis_list=bis32,
            character=char3,
            permissions=0,
            team=team1,
        )
        models.TeamMember.objects.create(
            bis_list=bis4,
            character=char4,
            permissions=0,
            team=team1,
        )

        team2 = models.Team.objects.create(
            invite_code=models.Team.generate_invite_code(),
            name='Team 2',
            tier=tier,
        )
        models.TeamMember.objects.create(
            bis_list=bis22,
            character=char2,
            permissions=0,
            team=team2,
        )
        models.TeamMember.objects.create(
            bis_list=bis33,
            character=char3,
            lead=True,
            team=team2,
        )
        models.TeamMember.objects.create(
            bis_list=bis4,
            character=char4,
            permissions=0,
            team=team2,
        )

        team3 = models.Team.objects.create(
            invite_code=models.Team.generate_invite_code(),
            name='Team 3',
            tier=tier,
        )
        models.TeamMember.objects.create(
            bis_list=bis23,
            character=char2,
            permissions=3,
            team=team3,
        )
        models.TeamMember.objects.create(
            bis_list=bis31,
            character=char3,
            lead=True,
            team=team3,
        )
        models.TeamMember.objects.create(
            bis_list=bis4,
            character=char4,
            permissions=0,
            team=team3,
        )

        print('Done! Visit http://localhost:8080/backend/admin to log in!')
