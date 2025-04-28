# api/serializers.py
from rest_framework import serializers
from .models import Sprint, Pros, Cons

class ProsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pros
        fields = ['id', 'user', 'text', 'created_at']

class ConsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cons
        fields = ['id', 'user', 'text', 'created_at']

class SprintSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    pros = ProsSerializer(many=True, read_only=True)
    cons = ConsSerializer(many=True, read_only=True)

    class Meta:
        model = Sprint
        fields = '__all__'

class DurationSerializer(serializers.Serializer):
    duration = serializers.IntegerField(min_value=1)

class ProsConsSerializer(serializers.Serializer):
    name = serializers.CharField()
    user_id = serializers.IntegerField()