from rest_framework.authtoken.models  import Token 
from datetime import timedelta 
from django.utils import timezone  
from django.contrib.auth.models import User 
from  .models import MySubscription  

def get_or_generate_token(user):
  token = Token.objects.filter(user=user)
  if token.exists():
    return token.first().key 
  token = Token(user=user) 
  token.save() 
  return token.key  

def perform_like(id,user_id,model,type="like"):
  # id => is for comment_id or reply_id
    
  user = User.objects.get(id=user_id)
  instance = model.objects.filter(id=id) 
  if not instance.exists():
    return 404 
  instance = instance.first() 
    
  if type == "unlike":
    if instance.unlikes.filter(id=user_id).exists():
      instance.unlikes.remove(user)
      return 204 
    instance.unlikes.add(user)
    return 201 
    
  if instance.likes.filter(id=user.id).exists():
    instance.likes.remove(user)
    return 204 
  instance.likes.add(user)
  return 201 

def perform_unlike(id,user_id,model,type="like"):
  return perform_like(id,user_id,model,type)



def add_my_subscription(user,subscription,payment):
  expire = None 
  if subscription.plan == "one-year":
    expire = timezone.now()+timedelta(days=365)
  if subscription.plan == "one-month":
    expire = timezone.now()+timedelta(days=29)
  if subscription.plan == "one-week":
    expire = timezone.now()+timedelta(days=7)
  my_subscription = MySubscription(user=user,payment=payment,subscription=subscription,expire=expire)
  my_subscription.save() 
  return my_subscription