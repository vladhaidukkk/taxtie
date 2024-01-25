import strawberry


def get_client():
    return "Strawberry"


@strawberry.type
class Query:
    client: str = strawberry.field(resolver=get_client)


schema = strawberry.Schema(Query)
