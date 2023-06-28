import strawberry

from gql.context import Info
from gql.resolvers.setting import getSettingByUser
from gql.resolvers.user import getDummy, getMe, getUser, getDetailedUser
from structs.graphql.auth import TokenData
from structs.graphql.user import DetailedUser, User, UserOut
from structs.graphql.setting import SettingOut


@strawberry.type
class Query:
    me: UserOut = strawberry.field(resolver=getMe, description='Get user profile data')

    user: User = strawberry.field(resolver=getUser, description='Get a user by id')

    detailedUser: DetailedUser = strawberry.field(resolver=getDetailedUser, description='Get a detailed user by id')

    setting: SettingOut = strawberry.field(resolver=getSettingByUser, description='Get user setting by userId')

    dummy: str = strawberry.field(resolver=getDummy)

    @strawberry.field
    def tokenData(self, info: Info) -> TokenData | None:
        return info.context.tokenData
