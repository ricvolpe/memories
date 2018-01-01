from rest_framework import serializers
from xmas_happiness_engine.models import Note

class NoteSerializer(serializers.Serializer):

    created = serializers.DateTimeField(format="%d/%m/%Y %H:%M", required=False)
    user = serializers.CharField(required=False)
    text = serializers.CharField()
    title = serializers.CharField()

    def create(self, validated_data):
        return Note.objects.create(**validated_data)
