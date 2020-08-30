from django.urls import path
from . import views


app_name='profiles'
urlpatterns = [
    path('myprofile/' , views.my_profile_view, name="my_profile"),
    path('invites/' , views.invites_received, name="my_invite"),
    path('login/', views.Loginpage, name="login"),
    path('registr_lis/', views.Registration , name="registr_view"),
    path('all_profile/', views.profiles_list_view, name="profiles_view"),
    path('invites_list/', views.invite_profile_list, name="invite_list"),
    path('all-profiles/', views.ProfileListView.as_view(),name="profile_list_view"),
    path('send-invite/', views.send_invatiation , name="send-invite"),
    path('removing_freind/', views.remove_from_friends, name="remove-freind"),
    path('invites/accept/', views.accept_invatition, name="accept-invite"),
    path('invites/reject/', views.reject_invatition , name="reject-invite"),
]
