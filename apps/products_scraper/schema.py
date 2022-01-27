from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from apps.products_scraper.models import Product
import graphene

class ProductTypeNode(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = ['id', 'name', 'original_price', 'sale_price', 'date']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    prodinfo = relay.Node.Field(ProductTypeNode)
    all_products = DjangoFilterConnectionField(ProductTypeNode)

    def products_info(self, info):
        return Product.objects.all()

schema = graphene.Schema(query=Query)
print("schema", schema)


# query {
#   allProducts {
#     edges {
#       node {
#         id
#         name
#         salePrice
#       }
#     }
#   }