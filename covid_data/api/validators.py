import re
from rest_framework import serializers
from .views import Message


def first_name_validator(value):
    """
    check if the provided name is valid or not
    :param value: first_name
    :return: first_name if it is correct
    """
    value = value.strip()
    if len(value) < 4:
        raise serializers.ValidationError(Message.code(4))
    if re.search(r'\d', value):
        raise serializers.ValidationError(Message.code(6))
    return value


def last_name_validator(value):
    """
    check if the provided name is valid or not
    :param value: last_name
    :return: last_name if it is correct
    """
    value = value.strip()
    if len(value) < 4:
        raise serializers.ValidationError(Message.code(5))
    if re.search(r'\d', value):
        raise serializers.ValidationError(Message.code(6))
    return value

