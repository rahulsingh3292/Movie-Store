from django.shortcuts import render 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User 
import random 
from rest_framework.generics import (ListAPIView,CreateAPIView,RetrieveAPIView,RetrieveUpdateAPIView,DestroyAPIView)
from rest_framework.views import APIView
from  .models import (Movie,Category,Actors,Language,Payment,MyMovies,Comment,Reply)
from  .import paytm 
from  .serializers import (MovieSerializer ,CategorySerilaizer,ActorSerializer,LanguageSerilaizer,PaymentHistorySerializer,CommentSerializer,ReplySerializer)
from  .detail_serializers import (CommentDetailSerializer,ReplyDetailSerializer,MovieDetailSerializer,MyMoviesSerializer)

from django.views.generic import View,TemplateView 
from  django.conf import settings 
from  django.views.decorators.csrf import csrf_exempt 
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response 

# Create your views here

class ActorCreateView(CreateAPIView):
  serializer_class = ActorSerializer 
  queryset = Actors.objects.all()
  authentication_classes=[BasicAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]

class ActorUpdateView(RetrieveUpdateAPIView):
  serializer_class = ActorSerializer
  queryset = Actors.objects.all() 
  authentication_classes=[BasicAuthentication]
  permission_classes = [IsAdminUser,IsAuthenticated]

class ActorDetailView(RetrieveAPIView):
  serializer_class = ActorUpdateView
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


class LanguageCreateView(CreateAPIView):
  serializer_class = LanguageSerilaizer
  queryset = Language.objects.all()
  authentication_classes=[BasicAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]
  

class LanguageUpdateView(RetrieveUpdateAPIView):
  serializer_class = LanguageSerilaizer
  queryset = Language.objects.all() 
  authentication_classes=[BasicAuthentication]
  permission_classes=[IsAdminUser,IsAuthenticated]
  lookup_field = "name"
  
  
class CategoryCreateView(CreateAPIView):
  serializer_class = CategorySerilaizer
  queryset = Category.objects.all()
  authentication_classes=[BasicAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]

class CategoryUpdateView(RetrieveUpdateAPIView):
  serializer_class = CategorySerilaizer 
  queryset = Category.objects.all()
  authentication_classes=[BasicAuthentication]
  permission_classes =[IsAdminUser,IsAuthenticated]
  lookup_field = "name"

class CategoryListView(ListAPIView):
  serializer_class = CategorySerilaizer 
  queryset = Category.objects.all() 
  
  
class CategoryDeleteView(DestroyAPIView):
  serializer_class = CategorySerilaizer
  queryset = Category.objects.all()
  authentication_classes=[BasicAuthentication]
  permission_classes = [IsAuthenticated,IsAdminUser]
  lookup_field = "name"
  
 
class MovieListView(ListAPIView):
  serializer_class = MovieSerializer
  queryset = Movie.objects.all()
  
class MovieCreateView(CreateAPIView):
  queryset = Movie.objects.all() 
  serializer_class = MovieSerializer 
  authentication_classes =[BasicAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]
  
class MovieDetailView(RetrieveAPIView):
  serializer_class = MovieDetailSerializer 
  queryset = Movie.objects.all() 
  
  def retrieve(self,request,*args,**kwargs):
    instance = super().get_object() 
    serializer = MovieDetailSerializer(instance)
    comment_serializer =  CommentDetailSerializer(Comment.objects.filter(movie=instance) ,many=True) 
    reply_serializer = ReplyDetailSerializer(Reply.objects.filter(movie=instance),many=True)
    return Response({"movie":serializer.data,"comments":comment_serializer.data,"replies":reply_serializer.data})
    
class MovieUpdateView(RetrieveUpdateAPIView):
  serializer_class = MovieSerializer
  queryset = Movie.objects.all()
  authentication_classes = [BasicAuthentication]
  permission_classes =[IsAuthenticated,IsAdminUser]

class MovieDeleteView(DestroyAPIView):
  serializer_class = MovieSerializer
  queryset = Movie.objects.all() 
  authentication_classes =[BasicAuthentication]
  permission_classes =[IsAdminUser,IsAuthenticated]


class PaymentHistoryView(ListAPIView):
  authentication_classes = [BasicAuthentication]
  permission_classes =[IsAuthenticated]
  
  def get_queryset(self,*args,**kwargs):
    return Payment.objects.filter(user=self.request.user)
  
  def list(self,request,*args,**kwargs):
    queryset = self.get_queryset()
    serializer = PaymentHistorySerializer(queryset,many=True)
    return Response(serializer.data,status=200)
  
  
class MyMoviesListView(ListAPIView):
  authentication_classes = [BasicAuthentication]
  permission_classes =[IsAuthenticated]
  
  def get_queryset(self,*args,**kwargs):
    return MyMovies.objects.filter(user=self.request.user)
  
  def list(self,request,*args,**kwargs):
    queryset = self.get_queryset() 
    serializer = MyMoviesSerializer(queryset,many=True)
    return Response(serializer.data,status=200)

class MyMovieDeleteView(DestroyAPIView):
  http_method_names = ['get','post', 'delete']
  authentication_classes = [BasicAuthentication]
  permission_classes = [IsAuthenticated]
  
  def get_object(self,*args,**kwargs):
    movie = MyMovies.objects.filter(id=self.kwargs["pk"])
    if movie.exists():
      movie = movie.first() 
      if movie.user == self.request.user:
        return movie 
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
  authentication_classes = [BasicAuthentication]
  permission_classes=[IsAuthenticated]
  
class CommentUpdateView(RetrieveUpdateAPIView):
  serializer_class = CommentSerializer 
  queryset = Comment.objects.all() 
  authentication_classes =[BasicAuthentication]
  permission_classes =[IsAuthenticated]
  
class CommentDeleteView(DestroyAPIView):
  serializer_class = CommentSerializer 
  queryset = Comment.objects.all() 
  authentication_classes =[BasicAuthentication]
  permission_classes=[IsAuthenticated]

class ReplyCreateView(CreateAPIView):
  serializer_class = ReplySerializer
  queryset = Reply.objects.all() 
  authentication_classes =[BasicAuthentication]
  permission_classes=[IsAuthenticated]
  
class ReplyUpdateView(RetrieveUpdateAPIView):
  serializer_class = ReplySerializer
  queryset = Reply.objects.all() 
  authentication_classes =[BasicAuthentication]
  permission_classes=[IsAuthenticated]

class ReplyDeleteView(DestroyAPIView):
  serializer_class = ReplySerializer
  queryset = Reply.objects.all() 
  authentication_classes =[BasicAuthentication]
  permission_classes=[IsAuthenticated]


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
  
  
class LikeCommentView(APIView):
  authentication_classes =[BasicAuthentication]
  permission_classes =[IsAuthenticated]
  http_method_names = ["post"]
  
  def post(self,request,format=None):
    like_resp = perform_like(request.data.get("id"),request.user.id,Comment)
    return Response({"status":like_resp})

class LikeReplyView(APIView):
  http_method_names =["post"]
  authentication_classes=[BasicAuthentication]
  permission_classes = [IsAuthenticated]
  
  def post(self,request,format=None):
    like_resp = perform_like(request.data.get("id"),request.user.id,Reply)
    return Response({"status":like_resp})
  

class UnLikeCommentView(APIView):
  http_method_names = ["post"]
  authentication_classes =[BasicAuthentication]
  permission_classes = [IsAuthenticated]
  
  def post(self,request,format=None):
    resp = perform_unlike(request.data.get("id"),request.user.id,Comment,"unlike")
    return Response({"status":resp})

  
class UnLikeReplyView(APIView):
  http_method_names=["post"]
  authentication_classes =[BasicAuthentication]
  permission_classes =[IsAuthenticated]
  
  def post(self,request,format=None):
    resp = perform_unlike(request.data.get("id"),request.user.id,Reply,"unlike")
    return Response({"status":resp})

def generateOrderId():
  return f"order{random.randint(1,90000000)}"
  
""" Here am using html(templates)  that's why i rendering to html page. if i`ll/you use ajax or any frontEnd framework/libraray then I'll/you-can send JsonResponse...
""" 
   
def checkout(request):
  amount = 10000
  # return JsonResponse({"amount":amount})
  return render(request,"checkout.html",{"amount":amount})
  
def delete_cookies(resp):
  resp.delete_cookie("email")
  resp.delete_cookie("movie_id")
  return 

class MovieBuyView(View):
  template_name = "paytm.html"
  
  def get(self,request):
    resp = render(request,template_name)
    delete_cookies(resp)
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
    #return JsonResponse(context)
    
    resp = render(request,"paytm.html",context)
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
      movie = Movie.objects.get(id=request.COOKIES["movie_id"])
      MyMovies.objects.create(user=transaction_data["user"],movie=movie)
     
      resp = render(request,"order_status.html",{"order_status":payment})
      delete_cookies(resp)
      return resp 
      
    if data["STATUS"] == "TXN_FAILURE":
      resp = render(request,"order_status.html",{"order_status":payment})
      delete_cookies(resp)
      return resp 
      
    return HttpResponse("Something went wrong..")
  
 
  checksum = request.POST.get("CHECKSUMHASH")
  if checksum:
      verify_checksum = Checksum.verifySignature(data,settings.MKEY,checksum)
      if not verify_checksum:
        return HttpResponse("Oops...something went wrong..")
   
  return render(request,"process_transaction.html",{"data":data})

   
  

  
