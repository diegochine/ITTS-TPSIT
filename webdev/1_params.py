from fastapi import FastAPI

app = FastAPI()
users = ('rick', 'morty', 'summer', 'beth', 'jerry', 'mr. poopybutthole')


@app.get("/users/")  # no parameters
async def all_users():
    """Return all users of the app."""
    return users


@app.get("/users/{user_id}")  # path parameter
async def user_from_id(user_id: int):
    """Returns user with provided ID"""
    return users[user_id]


@app.get("/users/filter/")
async def filter_users(letter: str, limit: int | None = None):  # query parameters
    """Filters users containing given letter"""
    filtered_users = list(filter(lambda u: letter in u, users))
    if limit is not None:
        filtered_users = filtered_users[:limit]
    return filtered_users
