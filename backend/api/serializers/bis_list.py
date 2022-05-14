"""
Serializer for BISList entries
"""
# lib
from rest_framework import serializers
# local
from api.models import BISList, Gear, Job
from .gear import GearSerializer
from .job import JobSerializer

__all__ = [
    'BISListSerializer',
    'BISListModifySerializer',
]


def _validate_gear_type(gear_type: str):
    """
    Function that returns a validation function for gear of a given type
    """
    def _inner(value: int) -> int:
        """
        Validate that the value is a Gear id that supports the required type
        """
        # Ensure valid id
        try:
            obj = Gear.objects.get(pk=value)
        except Gear.DoesNotExist:
            raise serializers.ValidationError('Please select a valid type of Gear.')

        # Ensure valid Gear for the slot
        if not getattr(obj, f'has_{gear_type}', False):
            raise serializers.ValidationError('The chosen type of Gear is invalid for this equipment slot.')

        return value
    return _inner


class BISListSerializer(serializers.ModelSerializer):
    bis_body = GearSerializer()
    bis_bracelet = GearSerializer()
    bis_earrings = GearSerializer()
    bis_feet = GearSerializer()
    bis_hands = GearSerializer()
    bis_head = GearSerializer()
    bis_left_ring = GearSerializer()
    bis_legs = GearSerializer()
    bis_mainhand = GearSerializer()
    bis_necklace = GearSerializer()
    bis_offhand = GearSerializer()
    bis_right_ring = GearSerializer()

    current_body = GearSerializer()
    current_bracelet = GearSerializer()
    current_earrings = GearSerializer()
    current_feet = GearSerializer()
    current_hands = GearSerializer()
    current_head = GearSerializer()
    current_left_ring = GearSerializer()
    current_legs = GearSerializer()
    current_mainhand = GearSerializer()
    current_necklace = GearSerializer()
    current_offhand = GearSerializer()
    current_right_ring = GearSerializer()
    item_level = serializers.IntegerField()
    job = JobSerializer()
    display_name = serializers.CharField()

    class Meta:
        exclude = ['owner']
        model = BISList


class BISListModifySerializer(serializers.ModelSerializer):
    offhand_is_mainhand = True

    job_id = serializers.CharField()  # Validate job first so offhand has it
    bis_body_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    bis_bracelet_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    bis_earrings_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    bis_feet_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    bis_hands_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    bis_head_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    bis_left_ring_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    bis_legs_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    bis_mainhand_id = serializers.IntegerField(validators=[_validate_gear_type('weapon')])
    bis_necklace_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    bis_offhand_id = serializers.IntegerField()
    bis_right_ring_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    current_body_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    current_bracelet_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    current_earrings_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    current_feet_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    current_hands_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    current_head_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    current_left_ring_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    current_legs_id = serializers.IntegerField(validators=[_validate_gear_type('armour')])
    current_mainhand_id = serializers.IntegerField(validators=[_validate_gear_type('weapon')])
    current_necklace_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    current_offhand_id = serializers.IntegerField()
    current_right_ring_id = serializers.IntegerField(validators=[_validate_gear_type('accessories')])
    external_link = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    name = serializers.CharField(max_length=64, allow_blank=True)

    class Meta:
        model = BISList
        fields = (
            'job_id',
            'bis_body_id',
            'bis_bracelet_id',
            'bis_earrings_id',
            'bis_feet_id',
            'bis_hands_id',
            'bis_head_id',
            'bis_left_ring_id',
            'bis_legs_id',
            'bis_mainhand_id',
            'bis_necklace_id',
            'bis_offhand_id',
            'bis_right_ring_id',
            'current_body_id',
            'current_bracelet_id',
            'current_earrings_id',
            'current_feet_id',
            'current_hands_id',
            'current_head_id',
            'current_left_ring_id',
            'current_legs_id',
            'current_mainhand_id',
            'current_necklace_id',
            'current_offhand_id',
            'current_right_ring_id',
            'external_link',
            'name',
        )
        extra_kwargs = {'bis_head_id': {'error_messages': {'invalid': 'Please select a valid type of Gear.'}}}

    def validate_job_id(self, job_id: str) -> str:
        """
        Check that the sent id is a valid string representing a job id
        """
        # Ensure it exists in the DB
        try:
            Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            raise serializers.ValidationError('Please select a valid Job.')

        # Check the flag
        if job_id == 'PLD':
            self.offhand_is_mainhand = False

        return job_id

    def validate_bis_offhand_id(self, bis_offhand: int) -> int:
        """
        If the job is paladin, run standard verification
        Otherwise just set this equal to the already validated mainhand value
        """
        if self.offhand_is_mainhand:
            bis_offhand = self.initial_data.get('bis_mainhand_id', -1)

        validator = _validate_gear_type('weapon')
        validator(bis_offhand)
        return bis_offhand

    def validate_current_offhand_id(self, current_offhand: int) -> int:
        """
        If the job is paladin, run standard verification
        Otherwise just set this equal to the already validated mainhand value
        """
        if self.offhand_is_mainhand:
            current_offhand = self.initial_data.get('current_mainhand_id', -1)

        validator = _validate_gear_type('weapon')
        validator(current_offhand)
        return current_offhand

    def validate_external_link(self, external_link):
        """
        Just some checking that if the URL is empty we return None
        """
        if external_link is None or str(external_link).strip() == '':
            return None
        return external_link
