from .import views
from django.urls import path

urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name='logout'),
    path('register/',views.registerPage,name="register"),

    path('', views.home,name='home_page'),
    path('data/',views.home,name='datas'),
    path('room/<str:pk>',views.RoomPage,name='room'),
    path('profile/<str:pk>',views.userProfile,name="userprofile"),

    path('create_room',views.createRoom,name="createroom"),
    path('update_room/<str:pk>',views.updateRoom,name="updateroom"),
    path('delete_room/<str:pk>',views.deleteRoom,name="deleteroom"),
    path('delete_message/<str:pk>',views.deleteMessage,name="deletemessage"),
    path('update_user',views.updateUser,name="updateuser"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity"),
]
