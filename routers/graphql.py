import strawberry
from strawberry.fastapi import GraphQLRouter

from gql.context import getContext
from gql.query import Query

schema = strawberry.Schema(query=Query)
router = GraphQLRouter(schema, context_getter=getContext, graphiql=True)
