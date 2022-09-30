## Our API

<blockquote class="quote warning">

### Beep Boop!

If you aren't a developer (who is proficient in programming), then the below documentation is not meant for you.

The documentation provided below provides the API (for developers who wish to leverage the Fates List API) and integrate it into their products.

</blockquote>

The Fates List API is fully open (*unlike most lists especially top.gg*). That is, the endpoints listed below are the endpoints used by the site itself. There are *no* site-only internal APIs.

That being sound our API itself does indeed use internal (not accessible by the public or the actual site) microservices such as silverpelt that serves to purely fetch and cache data sent from the discord API. Silverpelt is not publicly accessible whatsoever and should be considered as a implementation detail.

Silverpelt internally returns data using ``messagepack``. This is then serialized in the API (see below for the code for both the API, Silverpelt and the website) and can then be returned via the API to a user. This is actually how [Blazefire](#tag/Generic-endpoints/operation/get_discord_user) internally works.

### Fully Open Source!

Fates List is fully open source under the GNU AGPL3 license.

You can find the source code at [https://github.com/lunarsdev/fates-rewrite](https://github.com/lunarsdev/fates-rewrite).