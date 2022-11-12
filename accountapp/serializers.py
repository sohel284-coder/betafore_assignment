from rest_framework import serializers

from accountapp.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("This email is already exists")
        return lower_email

    class Meta:
        model = User
        fields = ("name", "email", "password", )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user



