from django.urls import path
from api import views

urlpatterns = [
    # BISLists
    path('character/<int:character_id>/bis_lists/', views.BISListCollection.as_view(), name='bis_collection'),
    path('character/<int:character_id>/bis_lists/<int:pk>/', views.BISListResource.as_view(), name='bis_resource'),
    path('character/<int:character_id>/bis_lists/<int:pk>/delete/', views.BISListDelete.as_view(), name='bis_delete'),

    # Character
    path('character/', views.CharacterCollection.as_view(), name='character_collection'),
    path('character/<int:pk>/', views.CharacterResource.as_view(), name='character_resource'),
    path('character/<int:pk>/delete/', views.CharacterDelete.as_view(), name='character_delete'),
    path('character/<int:pk>/verify/', views.CharacterVerification.as_view(), name='character_verification'),

    # Gear
    path('gear/', views.GearCollection.as_view(), name='gear_collection'),
    path('gear/item_levels/', views.ItemLevels.as_view(), name='item_levels'),

    # Imports
    path('import/etro/<str:id>/', views.EtroImport.as_view(), name='etro_import'),

    # Job
    path('job/', views.JobCollection.as_view(), name='job_collection'),

    # Loot
    path('team/<str:team_id>/loot/', views.LootCollection.as_view(), name='loot_collection'),
    path('team/<str:team_id>/loot/bis/', views.LootWithBIS.as_view(), name='loot_with_bis'),

    # Notifications
    path('notifications/', views.NotificationCollection.as_view(), name='notification_collection'),
    path('notifications/<int:pk>/', views.NotificationResource.as_view(), name='notification_resource'),

    # Team
    path('team/', views.TeamCollection.as_view(), name='team_collection'),
    path('team/<str:pk>/', views.TeamResource.as_view(), name='team_resource'),
    path('team/<str:team_id>/member/<int:pk>/', views.TeamMemberResource.as_view(), name='team_member_resource'),
    path('team/join/<str:invite_code>/', views.TeamInvite.as_view(), name='team_invite'),
    path('team/<str:pk>/permissions/', views.TeamPermissions.as_view(), name='team_permissions'),

    # Tier
    path('tier/', views.TierCollection.as_view(), name='tier_collection'),

    # UserView
    path('me/', views.UserView.as_view(), name='user'),
]
