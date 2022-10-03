SELECT DISTINCT bot_packs.id, bot_packs.icon, bot_packs.banner, 
bot_packs.created_at, bot_packs.owner, bot_packs.bots, 
bot_packs.description, bot_packs.name FROM (
    SELECT id, icon, banner, 
    created_at, owner, bots, 
    description, name, unnest(bots) AS bot_id FROM bot_packs
) bot_packs
INNER JOIN bots ON bots.bot_id = bot_packs.bot_id 
INNER JOIN users ON users.user_id = bot_packs.owner
WHERE bot_packs.name ilike $1 OR bot_packs.owner::text 
ilike $1 OR users.username ilike $1 OR bots.bot_id::text ilike $1 
OR bots.username_cached ilike $1