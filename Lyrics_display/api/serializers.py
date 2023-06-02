from rest_framework import serializers

class ParagraphSerializer(serializers.Serializer):
    paragraph = serializers.CharField()