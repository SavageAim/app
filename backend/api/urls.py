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
    path('import/plugin/', views.PluginImport.as_view(), name='plugin_import'),

    # Job
    path('job/', views.JobCollection.as_view(), name='job_collection'),
    path('job/solver/', views.JobSolverSortCollection.as_view(), name='job_solver_sort_collection'),

    # Lodestone Scraper Hooks
    path('lodestone/<str:character_id>/', views.LodestoneResource.as_view(), name='lodestone_resource'),
    path(
        'lodestone/<str:character_id>/import/<str:expected_job>/',
        views.LodestoneGearImport.as_view(),
        name='lodestone_gear_import',
    ),

    # Loot
    path('team/<str:team_id>/loot/', views.LootCollection.as_view(), name='loot_collection'),
    path('team/<str:team_id>/loot/delete/', views.LootDelete.as_view(), name='loot_delete'),
    path('team/<str:team_id>/loot/bis/', views.LootWithBIS.as_view(), name='loot_with_bis'),

    # LootSolver
    path('team/<str:team_id>/loot/solver/', views.LootSolver.as_view(), name='loot_solver'),

    # Notifications
    path('notifications/', views.NotificationCollection.as_view(), name='notification_collection'),
    path('notifications/<int:pk>/', views.NotificationResource.as_view(), name='notification_resource'),

    # Team
    path('team/', views.TeamCollection.as_view(), name='team_collection'),
    path('team/<str:pk>/', views.TeamResource.as_view(), name='team_resource'),
    path('team/<str:team_id>/member/<int:pk>/', views.TeamMemberResource.as_view(), name='team_member_resource'),
    path(
        'team/<str:team_id>/member/<int:pk>/permissions/',
        views.TeamMemberPermissionsResource.as_view(),
        name='team_member_permissions',
    ),
    path('team/join/<str:invite_code>/', views.TeamInvite.as_view(), name='team_invite'),

    # Team Proxy
    path('team/<str:team_id>/proxies/', views.TeamProxyCollection.as_view(), name='team_proxy_collection'),
    path('team/<str:team_id>/proxies/<int:pk>/', views.TeamProxyResource.as_view(), name='team_proxy_resource'),
    path('team/<str:team_id>/proxies/<int:pk>/claim/', views.TeamProxyClaim.as_view(), name='team_proxy_claim'),

    # Tier
    path('tier/', views.TierCollection.as_view(), name='tier_collection'),

    # UserView
    path('me/', views.UserView.as_view(), name='user'),
    path('me/token/', views.UserTokenView.as_view(), name='user_token'),
]
