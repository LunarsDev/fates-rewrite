SELECT DISTINCT bots.bot_id FROM bots 
INNER JOIN bot_owner ON bot_owner.bot_id = bots.bot_id 
WHERE bot_owner.owner = {} AND bot_owner.main = true