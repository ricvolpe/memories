from rest_framework import serializers
from xmas_happiness_engine.models import Note, Memory

class NoteSerializer(serializers.Serializer):

    created = serializers.DateTimeField(format="%d/%m/%Y %H:%M", required=False)
    user = serializers.CharField(required=False)
    text = serializers.CharField()
    title = serializers.CharField()
    linked = serializers.BooleanField(default=False)
    memory_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Memory.objects.all())

    def create(self, validated_data):
        return Note.objects.create(**validated_data)
