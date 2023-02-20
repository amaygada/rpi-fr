from rest_framework import serializers
from .models import *
from django.db import models
from rest_framework.validators import UniqueValidator


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("Name","Email", "Label",)
        extra_kwargs = {
            'Email': {
                'validators': [
                    UniqueValidator(
                        queryset=Person.objects.all()
                    )
                ]
            }
        }

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("PersonID", "Timestamp",)