from django.contrib import admin
from  .models import * 
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
  list_display =["id","name","release_date","price","categories","length"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display =["id","name"]

@admin.register(Actors)
class ActorsAdmin(admin.ModelAdmin):
  list_display =["id","first_name","last_name","dob","country"] 

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display =["id","user","TXNID","ORDERID","STATUS","TXNAMOUNT","BANKNAME","CHECKSUMHASH"]

@admin.register(MyMovies)
class MyMovieAdmin(admin.ModelAdmin):
  list_display = ["id","user","movie"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display =["id","movie","user","__str__"]
  
@admin.register(Reply)
class Reply(admin.ModelAdmin):
  list_display =["id","movie","user","comment","__str__"] 
  
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
  list_display = ["id","name"]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
  list_display =["id","price","plan"]

@admin.register(MySubscription)
class MySubscriptionAdmin(admin.ModelAdmin):
  list_display=["id","user","payment","subscription","expire"]
