from django.urls import path
from . import views


urlpatterns = [
    path('', views.display_log_reg),
    path('success',views.display_home),
    path('signup', views.new_sign_up),
    path('signin', views.new_sign_in),
    path('logout',views.destroy_session),
    path('add_an_event',views.add_new_event),
    path('addevent1',views.create_event),
    path('events/<int:evid>',views.show_event),
    path('event/<int:evid>/edit',views.show_edit),
    path('editevent/<int:evid>',views.updateevent),
    path('addcomment/<int:evid>',views.postcomment),
    path('comment/delete/<int:cmntid>',views.deletethiscomment),
    path('event/<int:evid>/delete',views.deletethisevent),
    path('returnhome',views.backhome),
    path('event/<int:evid>/favorite',views.favorite_this_book),
    path('event/<int:evid>/unfavorite',views.unfavorite_this_book),
    path('display_about_us',views.displyaboutus)
]