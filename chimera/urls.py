"""

__author__ = "Md Mazharul Islam Rakeb"
__email__ = "mislam7@uncc.edu"
__date__ = 9/15/21

"""
from django.conf.urls import url

from chimera import views

app_name = 'chimera'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^updateplan/', views.update_plan, name='updateplan'),
    url(r'^generate-deception-graph/', views.generate_deception_graph, name='generate_deception_graph'),
    url(r'^visualize-deception-graph/', views.visualize_deception_graph, name='visualize_deception_graph'),
    url(r'^recoaction/', views.recommend_optimal_action, name='recoaction'),
]
