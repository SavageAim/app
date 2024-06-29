"""
Serializers for Plugin imports
"""
# lib
from rest_framework import serializers

__all__ = [
    'PluginImportSerializer',
]


class PluginImportSlotSerializer(serializers.Serializer):
    name = serializers.CharField()
    item_level = serializers.IntegerField()


class PluginImportResponseSlotSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()


class PluginImportSerializer(serializers.Serializer):
    mainhand = PluginImportSlotSerializer()
    offhand = PluginImportSlotSerializer()
    head = PluginImportSlotSerializer()
    body = PluginImportSlotSerializer()
    hands = PluginImportSlotSerializer()
    legs = PluginImportSlotSerializer()
    feet = PluginImportSlotSerializer()
    earrings = PluginImportSlotSerializer()
    necklace = PluginImportSlotSerializer()
    bracelet = PluginImportSlotSerializer()
    right_ring = PluginImportSlotSerializer()
    left_ring = PluginImportSlotSerializer()


class PluginImportResponseSerializer(serializers.Serializer):
    mainhand = PluginImportResponseSlotSerializer(allow_null=True)
    offhand = PluginImportResponseSlotSerializer(allow_null=True)
    head = PluginImportResponseSlotSerializer(allow_null=True)
    body = PluginImportResponseSlotSerializer(allow_null=True)
    hands = PluginImportResponseSlotSerializer(allow_null=True)
    legs = PluginImportResponseSlotSerializer(allow_null=True)
    feet = PluginImportResponseSlotSerializer(allow_null=True)
    earrings = PluginImportResponseSlotSerializer(allow_null=True)
    necklace = PluginImportResponseSlotSerializer(allow_null=True)
    bracelet = PluginImportResponseSlotSerializer(allow_null=True)
    right_ring = PluginImportResponseSlotSerializer(allow_null=True)
    left_ring = PluginImportResponseSlotSerializer(allow_null=True)
