# Doc tags

from pydantic import BaseModel


class Tag(BaseModel):
    """A tag for a route (used for OpenAPI)"""

    name: str
    """The internal name of tag"""

    fname: str
    """The external name presented on API docs"""


bot = Tag(name="bot", fname="Bot-related endpoints")
server = Tag(name="server", fname="Server-related endpoints")
tests = Tag(name="tests", fname="Experimental test endpoints")
login = Tag(name="login", fname="Login")
generic = Tag(name="generic", fname="Generic endpoints")
user = Tag(name="user", fname="User-related endpoints")
data = Tag(name="data", fname="Data-related endpoints")

tags_metadata = [
    {
        "name": bot.fname,
        "description": "Operations related to bots",
    },
    {
        "name": tests.fname,
        "description": """Experimental test endpoints. 
        
These endpoints are not guaranteed to be stable and do not have to be implemented in any library/frontend 
(eg: ``Kitescratch`` and ``Sunbeam`` (the website))
""",
    },
    {
        "name": login.fname,
        "description": "Login-related endpoints",
    },
    {
        "name": generic.fname,
        "description": "Generic endpoints that don't fit into any other category",
    },
    {
        "name": user.fname,
        "description": "Operations related to users",
    },
    {
        "name": data.fname,
        "description": "Operations related to data (user data, to be specific)",
    },
]
