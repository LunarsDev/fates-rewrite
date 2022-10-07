/* 
Core search concepts:
To add a filter:

AND (bots.FIELD >= $N) -- FROM
AND (($N+1 = -1) OR (bots.FIELD <= $N+1)) -- TO
*/

SELECT DISTINCT bots.bot_id, bots.created_at, bots.description, bots.banner_card, bots.state, 
bots.votes, bots.flags, bots.guild_count FROM bots 
INNER JOIN bot_owner ON bots.bot_id = bot_owner.bot_id 
WHERE (bots.description ilike $1 
OR bots.long_description ilike $1 
OR bots.username_cached ilike $1 
OR bot_owner.owner::text ilike $1) 
AND (bots.state = $2 OR bots.state = $3) 
AND (cardinality($4::text[]) = 0 OR bots.tags {op} $4) -- Tags (either empty or do all tags in $4 exist in bots.tags)

-- Guild Count filter
AND (bots.guild_count >= $5)
AND (($6 = -1::bigint) OR (bots.guild_count <= $6))

-- Votes filter
AND (bots.votes >= $7)
AND (($8 = -1::bigint) OR (bots.votes <= $8))

ORDER BY bots.votes DESC, bots.guild_count DESC LIMIT 6