SELECT DISTINCT users.user_id, users.description FROM users 
INNER JOIN bot_owner ON users.user_id = bot_owner.owner 
INNER JOIN bots ON bot_owner.bot_id = bots.bot_id 
WHERE ((bots.state = $2 OR bots.state = $3) 
AND (bots.username_cached ilike $1 OR bots.description ilike $1 OR bots.bot_id::text ilike $1)) 
OR (users.username ilike $1) LIMIT 6