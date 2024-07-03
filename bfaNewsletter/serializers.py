from rest_framework import  serializers
from .models import Subscriber, EmailTemplate

class UserSerializer(serializers.HyperlinkedModelSerializer):
    model = Subscriber
    fields = '__all__'
    # lookup_field = 'slug'
    