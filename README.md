# Fates List Rewrite

## Components

### Backend

- ``Mapleshade`` - The core API implementations of fates list
- ``Silverpelt`` - A IPC service to handle all discord API actions (using fastapi and msgpack)

### Frontend

- ``Sunbeam`` - Fates List Frontend
- ``Kitescratch`` - Internal tooling including a simple CLI (`kitecli`) for Fates List (mostly for development, but may become a full cli-only replacement for sunbeam) as well as some helper functions including our test system (`kitehelper`) for developing Fates List

## Commits

- **All commits made to this repo must pass the tests (run ``kitehelper test``)

## Requirements

- Python 3.10+

## Running

1. Run ``uvicorn silverpelt.app:app --port 3030`` to start silverpelt
2. Then run ``uvicorn fates.app:app`` to start main API
3. **Either use nginx to serve the ``static`` folder (for all static assets) *or* (for local development ONLY) edit ``static`` in config.yaml to point to http://localhost:3030 and run ``python3 -m http.server 3030`` in the ``static`` folder**. This folder is not currently used.

## Database Seeding

Firstly apply piccolo migrations.

Then, pen ``psql``, then run the following:

```sql
\c fateslist

\copy bots FROM 'seed_data/seed.csv' DELIMITER ',' CSV;
```

## DB Changes

**Sept 12th 2022** 

- ``bot_library`` renamed to ``library`` (``ALTER TABLE bots RENAME COLUMN bot_library TO library``)
- Added vanity.id (``alter table vanity add column id SERIAL NOT NULL``)

## Developer Docs

### Kitescratch

- All API routes in ``fates`` must be implemented in ``api`` (and if possible, in ``views``)

### API Docs

- All styles should be in ``docs/styles.html`` *only*. This is to ensure that other users using the OpenAPI
specification also get decent styling (if their OpenAPI client supports CSS)

### Oauth2

In order for login to work, ``<YOUR DOMAIN>/frostpaw/login`` must be set in Discord Developer Portal as a Redirect URL for the Fates List bot configured in the ``secrets`` portion of ``config.yaml``.

### Routes

A simple route on Fates List would look like this:

```py
@route(
    Route(  
        app=app,
        mapleshade=mapleshade,
        url="/@bot",
        response_model=some_response_model_here,
        method=Method.get, # Route method
        tags=[tags.tests], # The tags of the route
        ratelimit=SharedRatelimit.new("core") # Or use a manual Ratelimit
    )
)
# NOTE that the request: Request bit is mandatory and @route will error if you don't give request as first parameter
async def route_name(request: Request, foo: int, bar: str):
    """FOO BAR"""
    # The below line for frostpaw-cache is in the case you dont have anything to do with a request
    if request.headers.get("Frostpaw-Cache"):
        raise HTTPException(400, detail="Caching via Frostpaw-Cache is not implemented")

    # Do something
```

Note that the ``route`` decorator checks all parameters passed to it and also enforces a basic structure for all routes.

### Errors

To handle a error, use a ``models.Response.error()``

**Example:**

```py
      if not auth_data:
            Response(
                done=False,
                reason="The specified server could not be found",
                code=ResponseCode.NOT_FOUND
            ).error(404)
```

For the case a ``HTTPException`` (etc) is raised instead, the ``route`` decorator automatically converts it into a ``Response`` and returns it however this leads to a broken ``code`` in the JSON and as such is discouraged.

## Authorization

Due to several issues (including extremely long URLs), the ``Frostpaw-Auth`` header is now the preferred way for authorization although ``/bots/{ID}/stats`` will still support ``Authorization`` as well as the new header.

**Format:**

``auth type (user/bot/server)|auth id|auth token``

**Example:**

``user|123456|abcdiskfh``

For endpoints, see https://api.fateslist.xyz/redoc

## Self Hosting

Fates List officially supports self hosting of our list and you can request for help on our [support server](https://fateslist.xyz/servers/789934742128558080).

This is the source code for [Fates List](https://fateslist.xyz/)

*BTW please add your bots there if you wish to support us. It would mean a lot!*

**We welcome all contributors and self hosters to Fates List**

### Domain Setup

1. Buy a domain (You will need a domain that can be added to Cloudflare in order to use Fates List. We use namecheap for this)

2. Add the domain to Cloudflare (see [this](https://support.cloudflare.com/hc/en-us/articles/201720164-Creating-a-Cloudflare-account-and-adding-a-website)). Our whole website requires Cloudflare as the DNS in order to work.

3. Buy a Linux VPS (You need a Linux VPS or a Linux home server with a public ip with port 443 open)

4. In Cloudflare, create a record (A/CNAME) called @ that points to your VPS ip/hostname

5. In Cloudflare, go to Speed > Optimization. Enable AMP Real URL

6. In Cloudflare, go to SSL/TLS, set the mode to Full (strict), enable Authenticated Origin Pull, make an origin certificate (in Origin Server) and save the private key as /key.pem on your VPS and the certificate as /cert.pem on your VPS

7. Download [https://support.cloudflare.com/hc/en-us/article_attachments/360044928032/origin-pull-ca.pem](https://support.cloudflare.com/hc/en-us/article_attachments/360044928032/origin-pull-ca.pem) and save it on the VPS as /origin-pull-ca.pem.

8. Repeat step for 4 with a A/CNAME record called lynx pointing to the same ip/hostname.

### Dependencies

- python 3.10 or newer
- go 1.18 or newer (for kitescratch)
- gcc-c++ (required for cython)
- libffi-devel (required for cython)
- libxslt-devel (required by some python dependencies we use such as lxml)
- libxml2-devel (required by some python dependencies we use such as lxml)- libpq-devel (required by some python dependencies we use such as asyncpg)
- docker
- docker-compose

## Custom Clients

Custom clients are supported however you are responsible for keeping them up-to-date. **See Kitescratch for a good example of how to do this**

