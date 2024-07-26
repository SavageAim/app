"""
The main class of the system;

Links together characters, jobs and gear into a single list
"""
from typing import List
import auto_prefetch
from django.db import models
from django.db.models import Q


class BISList(auto_prefetch.Model):
    bis_body = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_body_set')
    bis_bracelet = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_bracelet_set')
    bis_earrings = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_earrings_set')
    bis_feet = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_feet_set')
    bis_hands = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_hands_set')
    bis_head = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_head_set')
    bis_left_ring = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_left_ring_set')
    bis_legs = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_legs_set')
    bis_mainhand = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_mainhand_set')
    bis_necklace = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_necklace_set')
    bis_offhand = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_offhand_set')
    bis_right_ring = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_right_ring_set')

    current_body = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_body_set')
    current_bracelet = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_bracelet_set')
    current_earrings = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_earrings_set')
    current_feet = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_feet_set')
    current_hands = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_hands_set')
    current_head = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_head_set')
    current_left_ring = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_left_ring_set')
    current_legs = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_legs_set')
    current_mainhand = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_mainhand_set')
    current_necklace = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_necklace_set')
    current_offhand = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_offhand_set')
    current_right_ring = auto_prefetch.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_right_ring_set')
    external_link = models.URLField(null=True)
    job = auto_prefetch.ForeignKey('Job', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default='')
    owner = auto_prefetch.ForeignKey('Character', on_delete=models.CASCADE, related_name='bis_lists')

    class Meta(auto_prefetch.Model.Meta):
        ordering = ['-job__role', 'job__ordering', 'name']

    def __str__(self) -> str:
        return self.display_name

    def accessory_augments_required(self, gear_name: str) -> int:
        """
        Get a value of how many accessory augment tokens are needed for this BIS List
        """
        slots = [
            'earrings',
            'necklace',
            'bracelet',
            'right_ring',
            'left_ring',
        ]
        return self._check_augments(gear_name, slots)

    def armour_augments_required(self, gear_name: str) -> int:
        """
        Get a value of how many armour augment tokens are needed for this BIS List
        """
        slots = [
            'head',
            'body',
            'hands',
            'legs',
            'feet',
        ]
        return self._check_augments(gear_name, slots)

    def _check_augments(self, gear_name: str, slots: List[str]) -> int:
        """
        Check through slots, see how many of them need augmenting
        """
        needed = 0
        for slot in slots:
            current = getattr(self, f'current_{slot}')
            bis = getattr(self, f'bis_{slot}')
            if bis.name == gear_name and current.name != gear_name:
                needed += 1
        return needed

    def sync(self, to_sync: 'BISList'):
        """
        Given another list, sync the current gear from it to this one and save this one
        """
        self.current_mainhand = to_sync.current_mainhand
        self.current_offhand = to_sync.current_offhand
        self.current_head = to_sync.current_head
        self.current_body = to_sync.current_body
        self.current_hands = to_sync.current_hands
        self.current_legs = to_sync.current_legs
        self.current_feet = to_sync.current_feet
        self.current_earrings = to_sync.current_earrings
        self.current_necklace = to_sync.current_necklace
        self.current_bracelet = to_sync.current_bracelet
        self.current_left_ring = to_sync.current_left_ring
        self.current_right_ring = to_sync.current_right_ring
        self.save()

    @property
    def item_level(self):
        """
        Return the current item level of the job
        """
        return sum([
            self.current_body.item_level,
            self.current_bracelet.item_level,
            self.current_earrings.item_level,
            self.current_feet.item_level,
            self.current_hands.item_level,
            self.current_head.item_level,
            self.current_left_ring.item_level,
            self.current_legs.item_level,
            self.current_mainhand.item_level,
            self.current_necklace.item_level,
            self.current_offhand.item_level,
            self.current_right_ring.item_level,
        ]) / 12

    @property
    def display_name(self) -> str:
        """
        Same as Character, use the list name if one exists otherwise use the job name
        """
        if self.name != '':
            return self.name
        else:
            return self.job.display_name

    @staticmethod
    def needs_accessory_augments(gear_name: str) -> models.QuerySet:
        """
        Find any BIS Lists that require accessory augments, using the supplied name
        """
        return BISList.objects.select_related(
            'bis_earrings',
            'bis_necklace',
            'bis_bracelet',
            'bis_right_ring',
            'bis_left_ring',
            'current_earrings',
            'current_necklace',
            'current_bracelet',
            'current_right_ring',
            'current_left_ring',
            'job',
        ).filter(
            (Q(bis_earrings__name=gear_name) & ~Q(current_earrings__name=gear_name))
            | (Q(bis_necklace__name=gear_name) & ~Q(current_necklace__name=gear_name))
            | (Q(bis_bracelet__name=gear_name) & ~Q(current_bracelet__name=gear_name))
            | (Q(bis_right_ring__name=gear_name) & ~Q(current_right_ring__name=gear_name))
            | (Q(bis_left_ring__name=gear_name) & ~Q(current_left_ring__name=gear_name)),
        )

    @staticmethod
    def needs_armour_augments(gear_name: str) -> models.QuerySet:
        """
        Find any BIS Lists that require armour augments, using the supplied name
        """
        return BISList.objects.select_related(
            'bis_head',
            'bis_body',
            'bis_hands',
            'bis_legs',
            'bis_feet',
            'current_head',
            'current_body',
            'current_hands',
            'current_legs',
            'current_feet',
            'job',
        ).filter(
            (Q(bis_head__name=gear_name) & ~Q(current_head__name=gear_name))
            | (Q(bis_body__name=gear_name) & ~Q(current_body__name=gear_name))
            | (Q(bis_hands__name=gear_name) & ~Q(current_hands__name=gear_name))
            | (Q(bis_legs__name=gear_name) & ~Q(current_legs__name=gear_name))
            | (Q(bis_feet__name=gear_name) & ~Q(current_feet__name=gear_name)),
        )
