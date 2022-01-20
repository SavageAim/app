"""
The main class of the system;

Links together characters, jobs and gear into a single list

Currently is one gear list per character per job for ease, may change later
"""

from django.db import models


class BISList(models.Model):
    bis_body = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_body_set')
    bis_bracelet = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_bracelet_set')
    bis_earrings = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_earrings_set')
    bis_feet = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_feet_set')
    bis_hands = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_hands_set')
    bis_head = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_head_set')
    bis_left_ring = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_left_ring_set')
    bis_legs = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_legs_set')
    bis_mainhand = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_mainhand_set')
    bis_necklace = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_necklace_set')
    bis_offhand = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_offhand_set')
    bis_right_ring = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='bis_right_ring_set')

    current_body = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_body_set')
    current_bracelet = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_bracelet_set')
    current_earrings = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_earrings_set')
    current_feet = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_feet_set')
    current_hands = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_hands_set')
    current_head = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_head_set')
    current_left_ring = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_left_ring_set')
    current_legs = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_legs_set')
    current_mainhand = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_mainhand_set')
    current_necklace = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_necklace_set')
    current_offhand = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_offhand_set')
    current_right_ring = models.ForeignKey('Gear', on_delete=models.CASCADE, related_name='current_right_ring_set')
    external_link = models.URLField(null=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    owner = models.ForeignKey('Character', on_delete=models.CASCADE, related_name='bis_lists')

    class Meta:
        unique_together = ['job', 'owner']
        ordering = ['-job__role', 'job__ordering']

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
