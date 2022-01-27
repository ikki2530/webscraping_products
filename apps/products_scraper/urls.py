from django.conf.urls import url, include
from graphene_django.views import GraphQLView
from django.urls import path, include
from apps.products_scraper.views import fill_database
from . import schema


urlpatterns = [
    # path('graphql', GraphQLView.as_view(schema=schema, graphiql=True)), --> delete SCHEMA in settings
    path('graphql', GraphQLView.as_view(graphiql=True)),
    path('fill-database', fill_database, name='fill-database'),
]