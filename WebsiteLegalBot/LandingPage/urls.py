from django.urls import path
from . import views
from sentenceRetiever import views as testVIEW

urlpatterns = [
    path('', views.home, name='LegalBot-home'),
    path('about/', views.about, name='LegalBot-about'),
	path('orange/', views.orange, name='LegalBot-orange'),
	path('stats/', views.stats, name='LegalBot-stats'),
	path('results/', views.results, name='LegalBot-results'),
	path('docs/', views.docs, name='LegalBot-docs'),
	path('StatsDocumentation/', views.StatsDocumentation, name='LegalBot-StatsDocumentation'),
	path('OrangeDocumentation/', views.OrangeDocumentation, name='LegalBot-OrangeDocumentation'),
	path('WebsiteDocumentation/', views.WebsiteDocumentation, name='LegalBot-WebsiteDocumentation'),
	path('ProcessDocumentation/', views.ProcessDocumentation, name='LegalBot-ProcessDocumentation'),
]
