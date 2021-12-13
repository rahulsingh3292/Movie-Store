from django.urls import path 
from  .import views 

urlpatterns = [
    # list Api
    path("list/movies/",views.MovieListView.as_view()),
    
    path("list/category/",views.CategoryListView.as_view()),
   
    path("list/subscriptions/",views.SubscriptionsListView.as_view()),
    
    path("list/my-subscriptions/",views.MySubscriptionListView.as_view()),
    
    path("list/actors/",views.ActorListView.as_view()),
    
    path("list/my-movies/",views.MyMoviesListView.as_view()),
    
    # search  Api 
    
    path("search/movie/",views.MovieSearchView.as_view()),
    
    # Auth
    
    path("auth/login/",views.UserLoginView.as_view()),
  
    path("auth/register/",views.UserCreateView.as_view()), 
    
    # detail Api 
    path("detail/actor/<int:pk>/",views.ActorDetailView.as_view()),
    
    path("detail/user/<int:pk>/",views.UserDetailView.as_view()),
    
    path("detail/movie/<int:pk>/",views.MovieDetailView.as_view()),
    
    path("detail/my-movie/<int:pk>/",views.WatchMyMovieView.as_view()),
    
    path("detail/my-subscription/<int:pk>/",views.MySubscriptionDetailView.as_view()),
    
    path("detail/subscription/<int:pk>/",views.SubscriptionDetailView.as_view()),
    
    # update Api
    
    path("update/movie/<int:pk>/",views.MovieUpdateView.as_view()),
    
    path("update/user/<int:pk>/",views.UserUpdateView.as_view()),
    
    path("update/actor/<int:pk>/",views.ActorUpdateView.as_view()),
    
    path("update/language/<str:name>/",views.LanguageUpdateView.as_view()),
    
    path("update/category/<str:name>/",views.CategoryUpdateView.as_view()),
    
    path("update/comment/<int:pk>/",views.CommentUpdateView.as_view()),
    
    path("update/reply/<int:pk>/",views.ReplyUpdateView.as_view()),
    
    # create Api
    path("create/movie/",views.MovieCreateView.as_view()),
    
    path("create/category/",views.CategoryCreateView.as_view()),
    
    path("create/actor/",views.ActorCreateView.as_view()),
    
    path("create/language/",views.LanguageCreateView.as_view()),
    
    path("create/comment/",views.CommentCreateView.as_view()), 
    
    path("create/reply/",views.ReplyCreateView.as_view()), 
    
    # delete Api
    
    path("delete/category/<str:name>/",views.CategoryDeleteView.as_view()),
    
    path("delete/movie/<int:pk>/",views.MovieDeleteView.as_view()),
    
    path("delete/actor/<int:pk>/",views.ActorDeleteView.as_view()),
    
    path("delete/language/<str:name>/",views.LanguageDeleteView.as_view()),
    
    path("delete/my-movie/<int:pk>/",views.MyMovieDeleteView.as_view()),
   
    path("delete/user/<int:pk>/",views.UserDeleteView.as_view()),
   
    path("delete/comment/<int:pk>/",views.CommentDeleteView.as_view()),
    
    path("delete/reply/<int:pk>/",views.ReplyDeleteView.as_view()),
    # payment urls 
    path("movie/checkout/",views.checkout),
    
    path("subscription/",views.SubscriptionView.as_view()),
    
    path("pay/",views.MovieBuyView.as_view()),
    
    path("paytm-callback/",views.payment_response),
    
    
    path("history/payment/",views.PaymentHistoryView.as_view()),
    
    path("comment/like/",views.LikeCommentView.as_view()),
   
    path("comment/unlike/",views.UnLikeCommentView.as_view()),
   
    path("reply/like/",views.LikeReplyView.as_view()),
    
    path("reply/unlike/",views.UnLikeReplyView.as_view()),
    
    
  ]

