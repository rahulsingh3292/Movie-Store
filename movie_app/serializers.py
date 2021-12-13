from rest_framework import serializers
from  .models import Movie,Actors,Category,Language ,Payment,MyMovies,Comment ,Reply,User,Subscription
from django.contrib.auth.hashers import make_password 
from  rest_framework.authtoken.models import Token 



class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User 
    fields = ["username","email","first_name","last_name","password"]
    
  def create(self,validated_data):
    validated_data["password"] = make_password(validated_data["password"])
    instance = User(**validated_data)
    instance.save() 
    Token.objects.create(user=instance)
    return instance 
  
class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie 
    fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Actors 
    fields = "__all__"

class CategorySerilaizer(serializers.ModelSerializer):
  class Meta:
    model = Category 
    fields = "__all__"

class LanguageSerilaizer(serializers.ModelSerializer):
  class Meta:
    model = Language
    fields = "__all__"

class PaymentHistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment 
    fields = "__all__"

    
class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment 
    fields = "__all__"



class ReplySerializer(serializers.ModelSerializer):
  class Meta:
    model = Reply 
    fields = "__all__" 
    

class SubscriptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subscription 
    fields = "__all__"
    