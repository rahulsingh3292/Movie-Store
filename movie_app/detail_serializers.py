from rest_framework import serializers 
from  .models import Movie,Actors,Category,Language ,Payment,MyMovies,Comment ,Reply 

class MovieDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie 
    fields = "__all__"
    depth = 1 

class MyMoviesSerializer(serializers.ModelSerializer):
  class Meta:
    model = MyMovies 
    fields = "__all__"
    depth = 2 
    
class CommentDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment 
    fields = "__all__"
    depth = 1 

class ReplyDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reply 
    fields = "__all__"
    depth = 1 