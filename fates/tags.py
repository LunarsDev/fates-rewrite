# Doc tags

bot = "Bot-related endpoints"
tests = "Experimental test endpoints"
login = "Login"
generic = "Generic endpoints"
user = "User-related endpoints"
data = "Data-related endpoints"

tags_metadata = [
    {
        "name": bot,
        "description": "Operations related to bots",
    },
    {
        "name": tests,
        "description": """Experimental test endpoints. 
        
These endpoints are not guaranteed to be stable and do not have to be implemented in any library/frontend 
(eg: ``Kitescratch`` and ``Sunbeam`` (the website))
""",
    },
    {
        "name": login,
        "description": "Login-related endpoints",
    },
    {
        "name": generic,
        "description": "Generic endpoints that don't fit into any other category",
    },
    {
        "name": user,
        "description": "Operations related to users",
    },
    {
        "name": data,
        "description": "Operations related to data (user data, to be specific)",
    },
]