import strawberry

from resolvers.setting import getSettingByUser
from resolvers.user import getUser, getDetailedUser
from structs.graphql.user import DetailedUser, User
from structs.graphql.setting import Setting


@strawberry.type
class Query:
    user: User = strawberry.field(resolver=getUser, description='Get a user by id')

    detailedUser: DetailedUser = strawberry.field(resolver=getDetailedUser, description='Get a detailed user by id')

    setting: Setting = strawberry.field(resolver=getSettingByUser, description='Get user setting by userId')
