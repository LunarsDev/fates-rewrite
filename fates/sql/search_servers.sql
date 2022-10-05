/* 
Core search concepts:
To add a filter:

AND (servers.FIELD >= $N) -- FROM
AND (($N+1 = -1) OR (servers.FIELD <= $N+1)) -- TO
*/

SELECT DISTINCT servers.guild_id, servers.created_at, servers.description, servers.banner_card, 
servers.state, servers.votes, servers.guild_count, servers.flags FROM servers
WHERE (servers.description ilike $1
OR servers.long_description ilike $1
OR servers.name_cached ilike $1) 
AND (servers.state = $2 OR servers.state = $3)

-- Guild Count filter
AND (servers.guild_count >= $4)
AND (($5 = -1::bigint) OR (servers.guild_count <= $5))

-- Votes filter
AND (servers.votes >= $6)
AND (($7 = -1::bigint) OR (servers.votes <= $7))

ORDER BY servers.votes DESC, servers.guild_count DESC LIMIT 6