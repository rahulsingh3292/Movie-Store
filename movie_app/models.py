from django.db import models
from django.contrib.auth.models import User 


class Category(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name

COUNTRY = (("India","India"),("China","China"),("Korea","Korea"),("Brazil","Brazil"))


class Language(models.Model):
  name = models.CharField(max_length=200)
  country = models.CharField(max_length=150,choices=COUNTRY)
  
  
  def __str__(self):
    return self.name 
 
 
class Actors(models.Model):
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  dob = models.DateField(auto_now_add=True,blank=True,null=True)
  country = models.CharField(max_length=150,choices=COUNTRY)
  languages = models.ManyToManyField(Language,blank=True)
  
  
  def __str__(self):
    return  self.first_name + self.last_name


class Movie(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  url = models.SlugField(max_length=300,blank=True)
  price = models.FloatField(default=0.00)
  category = models.ManyToManyField(Category,blank=True)
  actors = models.ManyToManyField(Actors,blank=True)
  languages = models.ManyToManyField(Language,blank=True) 
  release_date = models.DateField(auto_now_add=True,blank=True,null=True)
  length = models.TimeField(blank=True,null=True)
  photo = models.ImageField(upload_to="Images/",blank=True,null=True)
  
  def __str__(self):
    return self.name 
  
  def categories(self):
    return str([i.name for i in self.category.all()])
  
      
  
  
class MyMovies(models.Model):
  movie = models.ForeignKey(Movie,on_delete=models.SET_NULL,null=True)
  user = models.ForeignKey(User,on_delete=models.CASCADE)

  
  def __str__(self):
    return self.user.username

class CommentCommon(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  description = models.TextField() 
  movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
  
  class Meta:
    abstract = True 
    
class Comment(CommentCommon):
  likes = models.ManyToManyField(User,blank=True,related_name="comment_likes")
  unlikes = models.ManyToManyField(User,blank=True,related_name="comment_unlikes")
  
  def __str__(self):
    return self.description[0:30]

  

class Reply(CommentCommon):
  comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
  likes = models.ManyToManyField(User,blank=True,related_name="reply_likes")
  unlikes = models.ManyToManyField(User,blank=True,related_name="reply_unlikes")
  
  def __str__(self):
    return self.description[0:30]
  
  


class Payment(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  ORDERID = models.CharField(max_length=150)
  TXNID = models.CharField(max_length=150)
  TXNAMOUNT= models.FloatField()
  CHECKSUMHASH = models.CharField(max_length=150,blank=True)
  BANKTXNID = models.CharField(max_length=150,blank=True)
  PAYMENTMODE = models.CharField(max_length=100,blank=True)
  TXNDATE = models.DateTimeField(auto_now_add=True,blank=True,null=True)
  BANKNAME = models.CharField(max_length=100,blank=True)
  RESPMSG = models.CharField(max_length=500,blank=True)
  STATUS = models.CharField(max_length=100,blank=True)
  
  def __str__(self):
    return self.user.username 
  