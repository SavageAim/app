"""
Serializer for Loot data
"""
# stdlib
from datetime import datetime
from string import capwords
from typing import Optional
# lib
from rest_framework import serializers
# local
from api.models import BISList, Loot, TeamMember

__all__ = [
    'LootSerializer',
    'LootCreateSerializer',
]

ITEMS = {
    'mainhand',
    # 'offhand',
    'head',
    'body',
    'hands',
    'legs',
    'feet',
    'earrings',
    'necklace',
    'bracelet',
    'ring',
}

EXTENDED_ITEMS = ITEMS | {
    'mount',
    'tome-weapon-token',
    'tome-weapon-augment',
    'tome-accessory-augment',
    'tome-armour-augment',
}


class LootSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    class Meta:
        exclude = ['tier', 'team']
        model = Loot

    def get_item(self, obj: Loot) -> str:
        """
        Turn the stored item field into a nice text display;
            - Capitalised words
            - Remove hyphens
        """
        return capwords(obj.item.replace('-', ' '))

    def get_member(self, obj: Loot) -> str:
        """
        We only need a name for the Member in the history so we'll get one
        """
        if obj.member is None:
            return 'Old Member'
        return f'{obj.member.character.name} @ {obj.member.character.world}'


class LootCreateSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField()

    class Meta:
        fields = ['member_id', 'item', 'greed', 'obtained']
        model = Loot

    def validate_member_id(self, member_id: int) -> TeamMember:
        """
        Ensure that the member id is valid and a member of the team in question
        """
        try:
            return self.context['team'].members.get(pk=member_id).pk
        except TeamMember.DoesNotExist:
            raise serializers.ValidationError('Please select a Character that is a member of the Team.')

    def validate_item(self, item: str) -> str:
        """
        All we can do here is check that the item sent is a valid name
        """
        if item not in EXTENDED_ITEMS:
            raise serializers.ValidationError('Please select a valid item.')
        return item

    def validate_obtained(self, obtained):
        """
        Ensure we're not recording loot for the future
        """
        if obtained > datetime.today().date():
            raise serializers.ValidationError('Cannot record loot for a date in the future.')
        return obtained


class LootCreateWithBISSerializer(serializers.Serializer):
    greed = serializers.BooleanField()
    greed_bis_id = serializers.IntegerField(required=False, allow_null=True)
    item = serializers.CharField()
    member_id = serializers.IntegerField()

    def validate_greed_bis_id(self, greed_bis_id: int) -> Optional[int]:
        """
        If sent, check that it's at least a BIS list belonging to a member of the team
        """
        if greed_bis_id is None:
            return None
        try:
            team_member_ids = self.context['team'].members.values_list('character_id', flat=True)
            BISList.objects.get(pk=greed_bis_id, owner_id__in=team_member_ids)
        except BISList.DoesNotExist:
            raise serializers.ValidationError('Please select a valid BIS List owned by a team member.')

        return greed_bis_id

    def validate_item(self, item: str) -> str:
        """
        All we can do here is check that the item sent is a valid name
        """
        if item not in ITEMS:
            raise serializers.ValidationError('Please select a valid item.')
        return item

    def validate_member_id(self, member_id: int) -> int:
        """
        Ensure that the member id is valid and a member of the team in question
        """
        try:
            self.context['team'].members.get(pk=member_id)
        except TeamMember.DoesNotExist:
            raise serializers.ValidationError('Please select a Character that is a member of the Team.')

        return member_id

    def validate(self, data):
        """
        Overlook checks;
            - Ensure that a greed bis id is set and valid if greed is true
            - Ensure that offhand is only set for a PLD BIS
        """
        bis: BISList
        if data['greed']:
            if data.get('greed_bis_id', None) is None:
                raise serializers.ValidationError({'greed_bis_id': 'This field is required for Greed loot entries.'})

            # Ensure the BIS belongs to the chosen member, and is not their team linked bis
            tm = TeamMember.objects.get(pk=data['member_id'])
            try:
                # Ensure the bis list belongs to the targeted character and is a greed list for this team
                bis = BISList.objects.get(
                    pk=data['greed_bis_id'],
                    owner=tm.character,
                )
            except BISList.DoesNotExist:
                raise serializers.ValidationError(
                    {'greed_bis_id': 'Please select a valid BIS List owned by a team member.'},
                )
            if bis.pk == tm.bis_list_id:
                raise serializers.ValidationError(
                    {'greed_bis_id': (
                        'To add Loot to the BIS List this Member has associated with the team, please set greed=false.'
                    )},
                )
        else:
            bis = self.context['team'].members.get(pk=data['member_id']).bis_list

        if data['item'] == 'offhand' and bis.job.id != 'PLD':
            raise serializers.ValidationError({'item': 'Offhand items can only be obtained by a PLD.'})

        # Also ensure that the requested item on bis in the list is actually the raid item
        raid_item = self.context['team'].tier.raid_gear_name
        if data['item'] == 'ring':
            # Check both rings for a raid ring for the tier
            if bis.bis_left_ring.name != raid_item and bis.bis_right_ring.name != raid_item:
                raise serializers.ValidationError(
                    {'item': 'The chosen item in the specified BIS List does not have the raid loot as its BIS.'},
                )
        else:
            if getattr(bis, f'bis_{data["item"]}').name != raid_item:
                raise serializers.ValidationError(
                    {'item': 'The chosen item in the specified BIS List does not have the raid loot as its BIS.'},
                )

        return data
