from rest_framework import serializers
from .models import MyUser


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'password', 'password2', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            phone=self.validated_data['phone']
            )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

class UserGetSerializer(serializers.ModelSerializer):
    class Meta():
        model = MyUser
        fields = ('first_name', 'email', 'phone')

class UserUpdateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ('first_name', 'phone', 'email')
        extra_kwargs = {'first_name': {'required': True}}

    def validate_email(self, value):
        user = self.context['request'].user
        if MyUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.phone = validated_data['phone']
        instance.email = validated_data['email']

        instance.save()

        return instance