from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('all-cohorts/', views.cohorts, name='cohort'),
    path('new-cohort/', views.create_cohort, name='new-cohort'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/edit/', views.edit_profile, name='edit-profile'),
    path('join_cohort/<id>', views.join_cohort, name='join-cohort'),
    path('leave_cohort/<id>', views.leave_cohort, name='leave-cohort'),
    path('single_cohort/<cohort_id>', views.single_cohort, name='single-cohort'),
    path('<cohort_id>/new-topic', views.create_topic, name='topic'),
    path('<cohort_id>/members', views.cohort_members, name='members'),
    path('search/', views.search_module, name='search'),
]
