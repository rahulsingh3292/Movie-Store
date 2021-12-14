from rest_framework import serializers 
from  .models import Movie,MyMovies,Comment,Reply ,Subscription,MySubscription,MovieActorRole,MoviesPhoto

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

class MySubscriptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = MySubscription 
    fields = "__all__"
    depth = 1
    
class ActorRoleDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = MovieActorRole  
    fields = "__all__"
    depth = 1 
    
class MoviesPhotosDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = MoviesPhoto 
    fields = "__all__"
    
    