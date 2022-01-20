"""
Serializer for a request user's information
"""
# lib
from rest_framework import serializers
# local
from api.models import Job

__all__ = [
    'JobSerializer',
]


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['ordering']
        model = Job
