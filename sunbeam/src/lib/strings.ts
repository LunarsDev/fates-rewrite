// W.I.P
// French and Italian translations by @azurex0001 [Azurex#0001]
// Next Up; Spanish & German

interface Translation {
  [lang: string]: string;
}

interface TranslationData {
  [key: string]: Translation;
}

interface TranslationReasonFunctions {
  [key: string]: (lang: string, s: string) => string;
}

// Reason parsers (only english supported for now)
export const reasons: TranslationReasonFunctions = {
  voted_recently: (lang: string, s: string) => {
    if (lang === 'en') {
      return `You have already voted recently, please wait ${s} seconds.`;
    }
    if (lang === 'fr') {
      return `Vous avez déjà voté récemment, veuillez attendre ${s} secondes.`;
    }
    if (lang === 'it') {
      return `Hai già votato di recente, attendi ${s} secondi.`;
    }
  }
};

// kitescratch-lint-start
// prettier-ignore
export const translations: TranslationData = {
 "ok": {
   "en": "ok",
   "fr": "ok",
   "it": "ok"
  },
 "auth_fail": {
   "en": "Authentication failed",
   "fr": "Échec de l'authentification",
   "it": "Autenticazione fallita"
  },
 "index.best_bots": {
   "en": "Find the best bots for your servers!",
   "fr": "Trouvez les meilleurs bots pour vos serveurs!",
   "it": "Trova i migliori bot per i tuoi server!",
   "__ignorable": "true"
  },
 "index.best_servers": {
   "en": "Find the best servers to join!",
   "fr": "Trouvez les meilleurs serveurs à rejoindre!",
   "it": "Trova i migliori server per unirsi!",
   "__ignorable": "true"
  },
 "index.search": {
   "en": "Search for the best bots and servers NOW!",
   "fr": "Recherchez les meilleurs bots et serveurs MAINTENANT!",
   "it": "Cerca i migliori bot e server ORA!",
   "__ignorable": "true"
  },
 "forbidden": {
   "en": "You are not allowed to do that!",
   "fr": "Vous n'êtes pas autorisé à faire cela!",
   "it": "Non sei autorizzato a fare quello!"
  },
 "not_found": {
   "en": "Hmmm... We couldn't find that!",
   "fr": "Hum... Nous n'avons pas trouvé ce que vous cherchez!",
   "it": "Hmmm... Non abbiamo trovato quello che stavi cercando!"
  },
 "unknown": {
   "en": "An unknown error occurred!",
   "fr": "Une erreur inconnue s'est produite!",
   "it": "Si è verificato un errore sconosciuto!"
  },
 "invalid_data": {
   "en": "Something went wrong! We have detected invalid fields!",
   "fr": "Quelque chose s'est mal passé! Nous avons détecté des champs invalides!",
   "it": "Qualcosa è andato storto! Abbiamo rilevato campi non validi!"
  },
 "login_required": {
   "en": "You need to be logged in to perform this action (joining login-only servers, adding bots)!",
   "fr": "Vous devez être connecté pour effectuer cette action (rejoindre des serveurs à accès limité, ajouter des bots)!",
   "it": "Devi essere connesso per eseguire questa azione (entrare in server a accesso limitato, aggiungere bot)!"
  },
 "private_server": {
   "en": "This server is private and not accepting invites at this time",
   "fr": "Ce serveur est privé et n'accepte pas les invitations pour le moment",
   "it": "Questo server è privato e non accetta inviti al momento"
  },
 "whitelist_only": {
  "en": "This server needs you to be whitelisted in order to join"
 },
 "blacklisted": {
  "en": "You are blacklisted from this server"
 },
 "server_blacklisted": {
   "en": "You are blacklisted from joining this server!",
   "fr": "Vous êtes banni de rejoindre ce serveur!",
   "it": "Sei bannato da questo server!"
 },
 "server_staff_review": {
   "en": "This server is currently under review by Fates List Staff and not accepting invites at this time!",
   "fr": "Ce serveur est actuellement en cours de révision par les membres du staff de Fates List et n'accepte pas les invitations pour le moment!",
   "it": "Questo server è attualmente in fase di revisione dallo staff di Fates List e non accetta inviti al momento!"
  },
 "server_banned": {
   "en": "This server has been banned (or denied due to requiring small changes) from Fates List. If you are a staff member of this server, contact Fates List Support for more information.",
   "fr": "Ce serveur a été banni (ou refusé en raison de demander des modifications mineures) de Fates List. Si vous êtes un membre du staff de ce serveur, contactez le support de Fates List pour plus d'informations.",
   "it": "Questo server è stato bannato (o negato a causa di richieste di modifiche piccole) da Fates List. Se sei un membro del staff di questo server, contatta il supporto di Fates List per ulteriori informazioni."
  },
 "server_no_channels": {
   "en": "Could not find channel to invite you to... Please ask the owner of this server to set an invite or set the invite channel for this server",
   "fr": "Impossible de trouver le channel pour vous fournir une invitation... Demandez au propriétaire de ce serveur de configurer un channel d'invitation ou définissez le channel d'invitation pour ce serveur",
   "it": "Impossibile trovare il canale per invitarti... Chiedi al proprietario di questo server di configurare un canale di invito o imposta il canale di invito per questo server"
  },
 "internal_error": {
   "en": "Whoa there! Something went wrong!",
   "fr": "Oups! Quelque chose s'est mal passé!",
   "it": "Oops! Qualcosa è andato storto!"
  },
 "bot_already_exists": {
   "en": "This bot already exists on Fates List",
   "fr": "Ce bot existe déjà sur Fates List",
   "it": "Questo bot esiste già su Fates List"
  },
 "prefix_too_long": {
   "en": "Prefix must be shorter than 9 characters",
   "fr": "Le préfix doit être plus court que 9 caractères",
   "it": "Il prefisso deve essere più corto di 9 caratteri"
  },
 "no_vanity": {
   "en": "You must have a vanity for your bot. This can be your username. You can prefix it with _ (underscore) if you don't want the extra growth from it. For example _mewbot would disable the mewbot vanity",
   "fr": "Vous devez avoir un vanity pour votre bot. Cela peut être votre pseudo. Vous pouvez le préfixer avec _ (underscore) si vous ne voulez pas l'extra-croissance de celui-ci. Par exemple _mewbot désactiverai le vanity mewbot",
   "it": "Devi avere un vanity per il tuo bot. Questo può essere il tuo username. Puoi prefissarlo con _ (underscore) se non vuoi l'extra-crescita di quello. Per esempio _mewbot disattiverà il vanity mewbot"
  },
 "vanity_taken": {
   "en": "This vanity has already been taken. Please contact Fates List staff if you wish to report this!",
   "fr": "Ce vanity a déjà été pris. Contactez le staff de Fates List si vous souhaitez signaler ceci!",
   "it": "Questo vanity è già stato preso. Contatta il staff di Fates List se vuoi segnalare questo!"
  },
 "invalid_invite_perms": {
   "en": "This invites permissions are invalid!",
   "fr": "Ces permissions d'invitation sont invalides!",
   "it": "Queste autorizzazioni per gli inviti sono invalide!"
  },
 "invalid_invite": {
   "en": "Your invite link must start with https: //",
   "fr": "Votre lien d'invitation doit commencer par https: //",
   "it": "Il tuo link di invito deve iniziare con https: //"
  },
 "invalid_description": {
   "en": "Your description must be at least 10 characters long and must be a maximum of 200 characters",
   "fr": "Votre description doit être d'au moins 10 caractères et ne doit pas dépasser 200 caractères",
   "it": "La tua descrizione deve essere di almeno 10 caratteri e non può superare i 200 caratteri"
  },
 "invalid_long_description": {
   "en": "Your long description must be at least 200 characters long",
   "fr": "Votre description longue doit être d'au moins 200 caractères",
   "it": "La tua descrizione lunga deve essere di almeno 200 caratteri"
  },
 "bot_not_found": {
   "en": "According to the Fates List API, your bot does not exist. Please try again after 2 hours.",
   "fr": "Selon l'API de Fates List, votre bot n'existe pas. Veuillez réessayer après 2 heures.",
   "it": "In base all'API di Fates List, il tuo bot non esiste. Riprova dopo 2 ore."
  },
 "no_tags": {
   "en": "You must select tags for your bot",
   "fr": "Vous devez sélectionner des tags pour votre bot",
   "it": "Devi selezionare i tag per il tuo bot"
  },
 "too_many_tags": {
   "en": "You can only select up to 10 tags for your bot",
   "fr": "Vous ne pouvez sélectionner un maximum de 10 tags pour votre bot",
   "it": "Puoi selezionare un massimo di 10 tag per il tuo bot"
  },
 "too_many_features": {
   "en": "You can only select up to 5 features for your bot",
   "fr": "Vous ne pouvez sélectionner qu'un maximum de 5 fonctionnalités pour votre bot",
   "it": "Puoi selezionare un massimo di 5 funzioni per il tuo bot"
  },
 "edit_locked": {
   "en": "This bot has either been locked by staff or has been edit locked by the main owner of the bot",
   "fr": "Ce bot a été bloqué par le staff ou a été bloqué par le propriétaire principal du bot",
   "it": "Questo bot è stato bloccato da staff o è stato bloccato da il proprietario principale del bot"
  },
 "too_many_owners": {
   "en": "The owner list is too long. You may only have a maximum of 5 extra owners",
   "fr": "La liste des propriétaires est trop longue. Vous ne pouvez avoir un maximum de 5 propriétaires supplémentaires",
   "it": "La lista dei proprietari è troppo lunga. Puoi avere un massimo di 5 proprietari extra"
  },
 "client_id_needed": {
   "en": "Client ID is required for this bot or is incorrect",
   "fr": "L'ID client est requis pour ce bot ou est incorrect",
   "it": "L'ID client è necessario per questo bot o è incorretto"
  },
 "invalid_client_id": {
   "en": "Client ID inputted is invalid for this bot",
   "fr": "L'ID client entré est invalide pour ce bot",
   "it": "L'ID client inserito è invalido per questo bot"
  },
 "private_bot": {
   "en": "This bot is private and cannot be added to Fates List",
   "fr": "Ce bot est privé et ne peut pas être ajouté à Fates List",
   "it": "Questo bot è privato e non può essere aggiunto a Fates List"
  },
 "invalid_owners": {
   "en": "You cannot add a main owner as an extra owner",
   "fr": "Vous ne pouvez pas ajouter un propriétaire principal comme propriétaire supplémentaire",
   "it": "Non puoi aggiungere un proprietario principale come proprietario extra"
  },
 "extra_link_val_length_err": {
   "en": "One of your extra link keys is too long",
   "fr": "Une de vos clés de lien supplémentaire est trop longue",
   "it": "Uno dei tuoi link extra è troppo lungo"
  },
 "extra_link_key_length_err": {
   "en": "One of your extra link values is too long",
   "fr": "Une de vos valeurs de lien supplémentaire est trop longue",
   "it": "Uno dei tuoi link extra è troppo lungo"
  },
 "extra_link_not_http": {
   "en": "One of your extra link values is not a valid URL (hint: check that its HTTPS and not HTTP)",
   "fr": "Une de vos valeurs de lien supplémentaire n'est pas une URL valide (indice: vérifiez qu'il s'agit d'un HTTPS et non d'un HTTP)"
  },
 "too_many_renderable_extra_links": {
   "en": "You have too many renderable extra links (extra links that do not start with an underscore)",
   "fr": "Vous avez trop de liens supplémentaires rendus (liens supplémentaires qui ne commencent pas par un underscore)",
   "it": "Hai troppi link extra renderizzabili (link extra che non iniziano con un underscore)"
  },
 "too_many_extra_links": {
   "en": "You have too many extra links. Try removing some?",
   "fr": "Vous avez trop de liens supplémentaires. Essayez de les enlever?",
   "it": "Hai troppi link extra. Prova a rimuoverne uno?"
  },
 "invalid_banner_page": {
   "en": "An error occurred while fetching the banner page for validation...",
   "fr": "Une erreur est survenue lors de la récupération de la page de bannière pour validation...",
   "it": "Si è verificato un errore durante il recupero della pagina banner per la validazione..."
  },
 "invalid_banner_card": {
   "en": "An error occurred while fetching the banner card for validation...",
   "fr": "Une erreur est survenue lors de la récupération de la carte de bannière pour validation...",
   "it": "Si è verificato un errore durante il recupero della carta banner per la validazione..."
  },
 "anti_abuse_error": {
   "en": "An error occurred while our anti-abuse provider handled your bot...",
   "fr": "Une erreur est survenue lors du traitement de votre bot par notre systeme d'anti-abus...",
   "it": "Si è verificato un errore durante il gestito dal nostro sistema anti-abuso..."
  },
 "not_main_owner": {
   "en": "This action needs you to be the main owner of this bot!"
  },
  "invalid_flag": {
   "en": "Illegal or otherwise non-edittable flag set on this profile",
   "fr": "Le flag est illégal ou non éditable",
   "it": "Il flag è illegale o non editabile"
  },
 "voted_recently": {
   "en": "You've already voted recently!",
   "fr": "Vous avez déjà voté récemment!",
   "it": "Hai già votato recentemente!"
  },
 "system_bot_vote": {
   "en": "This is a system bot or server and as such cannot be voted for at this time",
   "fr": "Ceci est un bot système ou serveur et ne peut pas être voté pour pour le moment",
   "it": "Questo è un bot o server di sistema quindi non può essere votato per il momento"
  },
 "vote_autorole_error": {
   "en": "For some odd reason, we have failed to give you autoroles for voting for this server. Are you on this server?",
   "fr": "Pour une raison inconnue, nous n'avons pas pu vous attribuer des rôles automatiquement lors de votre vote pour ce serveur. Êtes-vous sur ce serveur?",
   "it": "Per qualche motivo, non siamo riusciti a darti i ruoli automatici per votare per questo server. Sei su questo server?"
  },
  "not_implemented": {
   "en": "Whoa there! You aren't whitelisted to access this top-secret experiment yet!",
   "fr": "Whoa! Vous n'êtes pas autorisé à accéder à cet expérimentation secrète pour le moment!",
   "it": "Whoa! Non sei autorizzato ad accedere a questo sperimento segreto per il momento!"
  },
  "command_length_err": {
   "en": "This command is too long! Please try a shorter command name and/or description",
   "fr": "Cette commande est trop longue! Veuillez essayer un nom de commande et/ou une description plus courte",
   "it": "Questo comando è troppo lungo! Prova un comando più corto e/o una descrizione più corta"
  },
  "star_rating_err": {
   "en": "Star rating must be between 1 to 10. How did <em>this</em> happen?",
   "fr": "Le nombre d'étoiles doit être compris entre 1 et 10. Comment <em>ceci</em> est arrivé?",
   "it": "Il voto deve essere compreso tra 1 e 10. Come è capitato <em>questo</em>?"
  },
  "invalid_review_text": {
   "en": "Review text must be between 10 and 20000 characters long!",
   "fr": "Le texte de la critique doit être compris entre 10 et 20000 caractères!",
   "it": "Il testo della recensione deve essere compreso tra 10 e 20000 caratteri!"
  },
  "too_many_reviews": {
   "en": "You have already made a review for this bot. Please edit that instead!",
   "fr": "Vous avez déjà fait une critique pour ce bot. Veuillez la modifier à la place!",
   "it": "Hai già fatto una recensione per questo bot. Modificala invece!"
  },
  "invalid_parent_review": {
   "en": "The parent ID you are trying to reply to is invalid. How did <em>this</em> happen?",
   "fr": "L'ID du parent que vous essayez de répondre est invalide. Comment <em>ceci</em> est arrivé?",
   "it": "L'ID del parent che stai cercando di rispondere non è valido. Come è capitato <em>questo</em>?"
  },
  "review_alr_voted": {
   "en": "You have already voted for this review! Please change that instead?",
   "fr": "Vous avez déjà voté pour cette critique! Veuillez la changer à la place?",
   "it": "Hai già votato per questa recensione! Modificala invece?"
  },
 "invalid_appeal_text": {
   "en": "Appeal length must be between 7 and 4000 characters long!"
  },
 "bot_not_approved": {
   "en": "You cannot certify a bot/server that is not approved yet!"
  },
 "cert_no_banner_card": {
   "en": "You cannot certify a bot/server that has no banner for the bot card set yet! You can set one under 'Extras'"
  },
 "cert_no_banner_page": {
   "en": "You cannot certify a bot/server that has no banner for the bots page set yet! You can set one under 'Extras'"
  },
 "too_few_guilds": {
   "en": "You cannot certify a bot that is in less than 100 guilds!"
  },
 "too_few_members": {
   "en": "You cannot certify a server that has less than 100 members!"
  },
 "bad_stats": {
   "en": "Whoa there! You've got some nerve trying to post invalid stats to us!"
  },
 "too_many_subscriptions": {
   "en": "You have too many push notifications set up already! Please delete some before trying again!"
  },
 "too_many_bots_for_pack": {
   "en": "This pack has too many bots!"
  },
 "invalid_bot_id_for_pack": {
   "en": "This pack has an invalid bot ID!"
  },
 "too_few_bots_for_pack": {
   "en": "This pack has too few bots!"
  },
 "invalid_icon_for_pack": {
   "en": "This pack has an invalid icon URL!"
  },
 "invalid_banner_for_pack": {
   "en": "This pack has an invalid banner URL!"
  }
}
// kitescratch-lint-end

export function getIntlString(key: string, lang = 'en'): string {
  if (translations[key] && translations[key][lang]) {
    return translations[key][lang];
  } else if (translations[key] && translations[key]['en']) {
    return translations[key]['en'];
  } else {
    return key;
  }
}

export function getIntlReason(key: string): (lang: string, s: string) => string {
  if (reasons[key]) {
    return reasons[key];
  } else {
    // No reason found, return a function that returns the key

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    return (_: string, __: string) => {
      return '';
    };
  }
}

export function genError(json): string {
  const reason = getIntlReason(json['code']);

  return (
    getIntlString(json['code']) +
    '<br/><br/><br/>' +
    (reason('en', json['reason']) || json['reason'] || 'No context available...') +
    '</span>'
  );
}
