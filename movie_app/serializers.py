from rest_framework import serializers
from  .models import Movie,Actors,Category,Language ,Payment,MyMovies,Comment ,Reply

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
    

  