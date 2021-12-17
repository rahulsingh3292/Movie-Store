from django.shortcuts import render,redirect 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User 
from rest_framework.generics import (ListAPIView,CreateAPIView,RetrieveAPIView,RetrieveUpdateAPIView,DestroyAPIView)
from rest_framework.views import APIView
from  .models import (Movie,Category,Actors,Language,Payment,MyMovies,Comment,Reply,User,MySubscription,Subscription,MovieActorRole,MoviesPhoto)
from  .import paytm 
from  .serializers import (MovieSerializer ,CategorySerilaizer,ActorSerializer,LanguageSerilaizer,PaymentHistorySerializer,CommentSerializer,UserSerializer,ReplySerializer,SubscriptionSerializer)
import random
from  .serializers import ActorRoleSerializer,MoviesPhotoSerializer
from  .detail_serializers import (CommentDetailSerializer,ReplyDetailSerializer,MovieDetailSerializer,MyMoviesSerializer,MySubscriptionSerializer)
from  .detail_serializers import MoviesPhotosDetailSerializer,ActorRoleDetailSerializer
from django.views.generic import View,TemplateView 
from  django.conf import settings 
from  django.views.decorators.csrf import csrf_exempt 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response 
from rest_framework.filters import SearchFilter
from django.contrib.auth import authenticate
from  .import extras
# Create your views here


class UserLoginView(APIView):
  http_method_names=["post"]
  def post(self,request,format=None):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request,username=username,password=password)
    if user is not None:
      token = extras.get_or_generate_token(user)
      return Response({"result":"success","token":token},status=200)
    return Response({"result":"Invalid Credentials provided"},status=401)

class UserCreateView(CreateAPIView):
  serializer_class = UserSerializer
  queryset = User.objects.all() 

class UserUpdateView(RetrieveUpdateAPIView):
  serializer_class = UserSerializer 
  queryset = User.objects.all() 
  authentication_classes=[TokenAuthentication]
  permission_classes =[IsAuthenticated]
  

class UserDeleteView(DestroyAPIView):
  serializer_class = UserSerializer 
  queryset = User.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes =[IsAdminUser,IsAuthenticated]


class UserDetailView(RetrieveAPIView):
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAuthenticated]
   
  def get_object(self,*args,**kwargs):
    instance = User.objects.filter(id=self.kwargs["pk"]) 
    if instance.exists():
      instance = instance.first()
      if instance == self.request.user :
        return instance 
      return 403 
    return 404 
    
  
  def retrieve(self,request,*args,**kwargs):
    instance = self.get_object() 
    if instance == 404:
      return Response(status=404)
    if instance == 403:
      return Response(status=403)
      
    serializer = UserSerializer(instance)
    return Response(serializer.data,status=200)
 
class ActorCreateView(CreateAPIView):
  serializer_class = ActorSerializer 
  queryset = Actors.objects.all()
  authentication_classes=[TokenAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]

class ActorUpdateView(RetrieveUpdateAPIView):
  serializer_class = ActorSerializer
  queryset = Actors.objects.all() 
  authentication_classes=[TokenAuthentication]
  permission_classes = [IsAdminUser,IsAuthenticated]

class ActorDetailView(RetrieveAPIView):
  serializer_class = ActorSerializer
  queryset = Actors.objects.all()
  
  def retrieve(self,request,*args,**kwargs):
    instance = Actors.objects.filter(id=kwargs["pk"])
    if not instance.exists():
      return Response(status=404)
    instance = instance.first() 
    serializer = ActorSerializer(instance)
    actor_languages = [language.name for language in instance.languages.all()]
    actor_movies = MovieDetailSerializer(Movie.objects.filter(actors__id=instance.id),many=True)
    return Response({
      "actor":serializer.data,
      "actor_languages":actor_languages,
      "actor_movies":actor_movies.data},status=200)
  
class ActorListView(ListAPIView):
  serializer_class = ActorSerializer
  queryset = Actors.objects.all()

class ActorDeleteView(DestroyAPIView):
  serializer_class = ActorSerializer 
  queryset = Actors.objects.all()
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAuthenticated,IsAdminUser]

class ActorRoleCreateView(CreateAPIView):
  serializer_class = ActorRoleSerializer 
  queryset = MovieActorRole.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAdminUser,IsAuthenticated]



class LanguageCreateView(CreateAPIView):
  serializer_class = LanguageSerilaizer
  queryset = Language.objects.all()
  authentication_classes=[TokenAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]
  

class LanguageUpdateView(RetrieveUpdateAPIView):
  serializer_class = LanguageSerilaizer
  queryset = Language.objects.all() 
  authentication_classes=[TokenAuthentication]
  permission_classes=[IsAdminUser,IsAuthenticated]
  lookup_field = "name"
  
class LanguageDeleteView(DestroyAPIView):
  serializer_class = LanguageSerilaizer
  queryset = Language.objects.all()
  authentication_classes=[TokenAuthentication]
  permission_classes=[IsAuthenticated,IsAdminUser]
  lookup_field = "name"


class CategoryCreateView(CreateAPIView):
  serializer_class = CategorySerilaizer
  queryset = Category.objects.all()
  authentication_classes=[TokenAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]

class CategoryUpdateView(RetrieveUpdateAPIView):
  serializer_class = CategorySerilaizer 
  queryset = Category.objects.all()
  authentication_classes=[TokenAuthentication]
  permission_classes =[IsAdminUser,IsAuthenticated]
  lookup_field = "name"

class CategoryListView(ListAPIView):
  serializer_class = CategorySerilaizer 
  queryset = Category.objects.all() 
  
  
class CategoryDeleteView(DestroyAPIView):
  serializer_class = CategorySerilaizer
  queryset = Category.objects.all()
  authentication_classes=[TokenAuthentication]
  permission_classes = [IsAuthenticated,IsAdminUser]
  lookup_field = "name"
  
 
class MovieListView(ListAPIView):
  serializer_class = MovieSerializer
  queryset = Movie.objects.all()
  
class MovieCreateView(CreateAPIView):
  queryset = Movie.objects.all() 
  serializer_class = MovieSerializer 
  authentication_classes =[TokenAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]
  
class MovieDetailView(RetrieveAPIView):
  serializer_class = MovieDetailSerializer 
  queryset = Movie.objects.all() 
  
  def retrieve(self,request,*args,**kwargs):
    instance = super().get_object() 
    serializer = MovieDetailSerializer(instance)
    comment_serializer =  CommentDetailSerializer(Comment.objects.filter(movie=instance) ,many=True) 
    movie_photos = MoviesPhotosDetailSerializer(MoviesPhoto.objects.filter(movie=instance),many=True)
    actor_roles = ActorRoleDetailSerializer(MovieActorRole.objects.filter(movie=instance),many=True)
    reply_serializer = ReplyDetailSerializer(Reply.objects.filter(movie=instance),many=True)
    is_premium_member = False
    if request.user.is_authenticated:
      is_premium_member = MySubscription.objects.filter(user=request.user).exists()
      
    return Response({"movie":serializer.data,"comments":comment_serializer.data,"replies":reply_serializer.data,"is_premium_member":is_premium_member,"actor_roles":actor_roles.data,"movie_photos":movie_photos.data})
    
class MovieUpdateView(RetrieveUpdateAPIView):
  serializer_class = MovieSerializer
  queryset = Movie.objects.all()
  authentication_classes = [TokenAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]

class MovieDeleteView(DestroyAPIView):
  serializer_class = MovieSerializer
  queryset = Movie.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes =[IsAdminUser,IsAuthenticated]
  
class MoviesPhotoCreateView(CreateAPIView):
  serializer_class = MoviesPhotoSerializer 
  queryset = MoviesPhoto.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAuthenticated,IsAdminUser]


class PaymentHistoryView(ListAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes =[IsAuthenticated]
  
  def get_queryset(self,*args,**kwargs):
    return Payment.objects.filter(user=self.request.user)
  
  def list(self,request,*args,**kwargs):
    queryset = self.get_queryset()
    serializer = PaymentHistorySerializer(queryset,many=True)
    return Response(serializer.data,status=200)
  
  
class MyMoviesListView(ListAPIView):
  authentication_classes = [TokenAuthentication]
  permission_classes =[IsAuthenticated]
  
  def get_queryset(self,*args,**kwargs):
    return MyMovies.objects.filter(user=self.request.user)
  
  def list(self,request,*args,**kwargs):
    queryset = self.get_queryset() 
    serializer = MyMoviesSerializer(queryset,many=True)
    return Response(serializer.data,status=200)

class MyMovieDeleteView(DestroyAPIView):
  http_method_names = ['get','post', 'delete']
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  
  def get_object(self,*args,**kwargs):
    instance = MyMovies.objects.filter(id=self.kwargs["pk"]) 
    if instance.exists():
      instance = instance.first()
      if instance.user == self.request.user :
        return instance 
      return 403 
    return 404 
 

  def destroy(self,request,*args,**kwargs):
    instance = self.get_object() 
    if instance == 404:
      return Response(status=404)
    if instance == 403:
      return Response(status=403)
    instance.delete() 
    return Response(status=200)
    
class CommentCreateView(CreateAPIView):
  serializer_class = CommentSerializer 
  queryset = Comment.objects.all() 
  authentication_classes = [TokenAuthentication]
  permission_classes=[IsAuthenticated]
  
class CommentUpdateView(RetrieveUpdateAPIView):
  serializer_class = CommentSerializer 
  queryset = Comment.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes =[IsAuthenticated]
  
class CommentDeleteView(DestroyAPIView):
  serializer_class = CommentSerializer 
  queryset = Comment.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAuthenticated]

class ReplyCreateView(CreateAPIView):
  serializer_class = ReplySerializer
  queryset = Reply.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAuthenticated]
  
class ReplyUpdateView(RetrieveUpdateAPIView):
  serializer_class = ReplySerializer
  queryset = Reply.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAuthenticated]

class ReplyDeleteView(DestroyAPIView):
  serializer_class = ReplySerializer
  queryset = Reply.objects.all() 
  authentication_classes =[TokenAuthentication]
  permission_classes=[IsAuthenticated]

  
  
class LikeCommentView(APIView):
  authentication_classes =[TokenAuthentication]
  permission_classes =[IsAuthenticated]
  http_method_names = ["post"]
  
  def post(self,request,format=None):
    like_resp = extras.perform_like(request.data.get("id"),request.user.id,Comment)
    return Response({"status":like_resp})

class LikeReplyView(APIView):
  http_method_names =["post"]
  authentication_classes=[TokenAuthentication]
  permission_classes = [IsAuthenticated]
  
  def post(self,request,format=None):
    like_resp = extras.perform_like(request.data.get("id"),request.user.id,Reply)
    return Response({"status":like_resp})
  

class UnLikeCommentView(APIView):
  http_method_names = ["post"]
  authentication_classes =[TokenAuthentication]
  permission_classes = [IsAuthenticated]
  
  def post(self,request,format=None):
    resp = extras.perform_unlike(request.data.get("id"),request.user.id,Comment,"unlike")
    return Response({"status":resp})

  
class UnLikeReplyView(APIView):
  http_method_names=["post"]
  authentication_classes =[TokenAuthentication]
  permission_classes =[IsAuthenticated]
  
  def post(self,request,format=None):
    resp = extras.perform_unlike(request.data.get("id"),request.user.id,Reply,"unlike")
    return Response({"status":resp})


class MovieSearchView(ListAPIView):
  serializer_class = MovieDetailSerializer 
  queryset = Movie.objects.all()
  filter_backends =[SearchFilter]
  # symbol ==> ^ start with , = extact match
  search_fields = ["^name","=languages__name","=category__name","=country"]
  
class WatchMyMovieView(RetrieveAPIView):
  authentication_classes=[TokenAuthentication]
  permission_classes=[IsAuthenticated]
  
  def get_object(self,*args,**kwargs):
    instance = MyMovies.objects.filter(id=self.kwargs["pk"]) 
    if instance.exists():
      instance = instance.first()
      if instance.user == self.request.user :
        return instance 
      return 403 
    return 404 
  
  def retrieve(self,request,*args,**kwargs):
    instance = self.get_object() 
    if instance == 404:
      return Response(status=404)
    if instance == 403:
      return Response(status=403)
    serializer = MyMoviesSerializer(instance)
    return Response(serializer.data,status=200)

class SubscriptionsListView(ListAPIView):
  serializer_class = SubscriptionSerializer 
  queryset = Subscription.objects.all() 

class SubscriptionDetailView(RetrieveAPIView):
  serializer_class = SubscriptionSerializer 
  queryset = Subscription.objects.all() 

class MySubscriptionListView(ListAPIView):
  authentication_classes=[TokenAuthentication]
  permission_classes=[IsAuthenticated]
  
  def get_queryset(self):
    return MySubscription.objects.filter(user=self.request.user)
  
  def list(self,request,*args,**kwargs):
    queryset = self.get_queryset() 
    serializer = MySubscriptionSerializer(queryset,many=True)
    return Response(serializer.data,status=200)

class MySubscriptionDetailView(RetrieveAPIView):
  authentication_classes =[TokenAuthentication]
  permission_classes =[IsAuthenticated]
  
  def get_object(self,*args,**kwargs):
    instance = MySubscription.objects.filter(id=self.kwargs["pk"]) 
    if instance.exists():
      instance = instance.first()
      if instance.user == self.request.user :
        return instance 
      return 403 
    return 404 
  
  def retrieve(self,request,*args,**kwargs):
    instance = self.get_object() 
    if instance == 404:
      return Response(status=404)
    if instance == 403:
      return Response(status=403)
    serializer = MySubscriptionSerializer(instance)
    return Response(serializer.data,status=200)
  

def generateOrderId():
  return f"order{random.randint(1,90000000)}"
  
""" Here am using html(templates).
  that's why i rendering to html page.
  if i`ll/you use ajax or any
  frontEnd framework/libraray then 
  I'll/you-can send JsonResponse...
""" 

# Movie checkout
def checkout(request):
  # movie checkout page 
  amount = 10000
  # return JsonResponse({"amount":amount})
  return render(request,"checkout.html",{"amount":amount})
  

class SubscriptionView(View):
  def get(self,request):
    resp = render(request,"subscription.html")
    return resp 
  
  def post(self,request):
    context ={}
 
    plan = self.request.POST.get("plan")
    
    subscription = Subscription.objects.filter(plan=plan)
    if not subscription.exists():
      return HttpResponse("No subscription")
    subscription = subscription.first()
    amount = subscription.price
    if subscription.discount:
      amount -= subscription.discount 
    orderId = generateOrderId()
    context["txnToken"] = paytm.initiateTransaction(amount,orderId)
    
    context ["orderId"] = orderId 
    context["mid"] = settings.MID
    if not context["txnToken"]:
      # JsonResponse
      return HttpResponse("payment failure or system error.. plaese try again..")
    context["subscription"] = plan
    resp = render(request,"paytm.html",context)
    resp.delete_cookie("movie_id")
    resp.set_cookie("subscription",plan)
    resp.set_cookie("email",request.user.email)
    return resp 


class MovieBuyView(View):
  template_name = "paytm.html"
  
  def get(self,request):
    resp = render(request,template_name)
    return resp 
  
  def post(self,request):
    context = {}
    amount =request.POST.get("amount")
    movie_id = request.POST.get("movie_id")
    if not amount:
      # here you can send JsonResponse
      return HttpResponse("Amount not declared")
    orderId = generateOrderId()
    context["txnToken"] = paytm.initiateTransaction(amount,orderId)
    context ["orderId"] = orderId 
    context["mid"] = settings.MID
    if not context["txnToken"]:
      # JsonResponse
      return HttpResponse("payment failure or system error.. plaese try again..")
      
    # send json data 
    # return JsonResponse(context)
    
    resp = render(request,"paytm.html",context)
    resp.delete_cookie("plan")
    resp.set_cookie("email",request.user.email)
    resp.set_cookie("movie_id",movie_id)
    return resp 


@csrf_exempt 
def payment_response(request):
  if request.method == "POST":
    data = request.POST.dict() 
    transaction_data = dict({(key,value) for key,value in data.items() if hasattr(Payment(),key)})
    transaction_data["user"] = User.objects.get(email=request.COOKIES["email"])
    payment = Payment(**transaction_data)
    payment.save() 
    if data["STATUS"] == "TXN_SUCCESS":
      # User Buyed Movie 
      if request.COOKIES.get("movie_id"):
        movie = Movie.objects.get(id=request.COOKIES["movie_id"])
        MyMovies.objects.create(user=transaction_data["user"],movie=movie)
      
        return JsonResponse({"result":"Movie addedd"})
        
        
      if request.COOKIES.get("subscription"):
        subscription = Subscription.objects.get(plan=request.COOKIES["subscription"])
        extras.add_my_subscription(transaction_data["user"],subscription,payment)
        return JsonResponse({"result":"Subscription done"})
        
      
    if data["STATUS"] == "TXN_FAILURE":
      if request.COOKIES.get("subscription"):
        return JsonResponse({"result":"Subscription Failed"})
      return JsonResponse({"result":"movie buying Failed"})

 
  checksum = request.POST.get("CHECKSUMHASH")
  if checksum:
      verify_checksum = Checksum.verifySignature(data,settings.MKEY,checksum)
      if not verify_checksum:
        return JsonResponse({"something went wrong"})
   
  return render(request,"process_transaction.html",{"data":data})

  
