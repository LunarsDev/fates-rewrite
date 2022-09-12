interface Translation {
  [lang: string]: string;
}

interface TranslationData {
  [key: string]: Translation;
}

// W.I.P
// French and Italian translations by @azurex0001 [Azurex#0001]
// Next Up; Spanish & German

export const translations: TranslationData = {
  'index.best_bots': {
    en: 'Find the best bots for your servers!',
    fr: 'Trouvez les meilleurs bots pour vos serveurs!',
    it: 'Trova i migliori bot per i tuoi server!'
  },
  'index.best_servers': {
    en: 'Find the best servers to join!',
    fr: 'Trouvez les meilleurs serveurs à rejoindre!',
    it: 'Trova i migliori server per unirsi!'
  },
  'index.search': {
    en: 'Search for the best bots and servers NOW!',
    fr: 'Recherchez les meilleurs bots et serveurs MAINTENANT!',
    it: 'Cerca i migliori bot e server ORA!'
  },
  MemberNotFound: {
    en: 'You are not on our support server!',
    fr: "Vous n'êtes pas sur notre serveur de support!",
    it: 'Non sei sul nostro server di supporto!'
  },
  Forbidden: {
    en: 'You are not allowed to do that!',
    fr: "Vous n'êtes pas autorisé à faire cela!",
    it: 'Non sei autorizzato a fare quello!'
  },
  NotFound: {
    en: "Hmmm... We couldn't find that!",
    fr: "Hum... Nous n'avons pas trouvé ce que vous cherchez!",
    it: 'Hmmm... Non abbiamo trovato quello che stavi cercando!'
  },
  InvalidFields: {
    en: 'Something went wrong! We have detected invalid fields!',
    fr: "Quelque chose s'est mal passé! Nous avons détecté des champs invalides!",
    it: 'Qualcosa è andato storto! Abbiamo rilevato campi non validi!'
  },
  LoginRequired: {
    en: 'You need to be logged in to perform this action (joining login-only servers, adding bots)!',
    fr: 'Vous devez être connecté pour effectuer cette action (rejoindre des serveurs à accès limité, ajouter des bots)!',
    it: 'Devi essere connesso per eseguire questa azione (entrare in server a accesso limitato, aggiungere bot)!'
  },
  NotAcceptingInvites: {
    en: 'This server is private and not accepting invites at this time',
    fr: "Ce serveur est privé et n'accepte pas les invitations pour le moment",
    it: 'Questo server è privato e non accetta inviti al momento'
  },
  Blacklisted: {
    en: 'You are blacklisted from joining this server!',
    fr: 'Vous êtes banni de rejoindre ce serveur!',
    it: 'Sei bannato da questo server!'
  },
  StaffReview: {
    en: 'This server is currently under review by Fates List Staff and not accepting invites at this time!',
    fr: "Ce serveur est actuellement en cours de révision par les membres du staff de Fates List et n'accepte pas les invitations pour le moment!",
    it: 'Questo server è attualmente in fase di revisione dallo staff di Fates List e non accetta inviti al momento!'
  },
  ServerBanned: {
    en: 'This server has been banned (or denied due to requiring small changes) from Fates List. If you are a staff member of this server, contact Fates List Support for more information.',
    fr: "Ce serveur a été banni (ou refusé en raison de demander des modifications mineures) de Fates List. Si vous êtes un membre du staff de ce serveur, contactez le support de Fates List pour plus d'informations.",
    it: 'Questo server è stato bannato (o negato a causa di richieste di modifiche piccole) da Fates List. Se sei un membro del staff di questo server, contatta il supporto di Fates List per ulteriori informazioni.'
  },
  NoChannelFound: {
    en: 'Could not find channel to invite you to... Please ask the owner of this server to set an invite or set the invite channel for this server',
    fr: "Impossible de trouver le channel pour vous fournir une invitation... Demandez au propriétaire de ce serveur de configurer un channel d'invitation ou définissez le channel d'invitation pour ce serveur",
    it: 'Impossibile trovare il canale per invitarti... Chiedi al proprietario di questo server di configurare un canale di invito o imposta il canale di invito per questo server'
  },
  SQLError: {
    en: 'Whoa there! Something went wrong! We have detected a SQL error!',
    fr: "Oups! Quelque chose s'est mal passé! Nous avons détecté une erreur SQL!",
    it: 'Oops! Qualcosa è andato storto! Abbiamo rilevato un errore SQL!'
  },
  RequestError: {
    en: 'Something went wrong in our internal connections! Please try again later!',
    fr: "Quelque chose s'est mal passé dans nos connexions internes! Veuillez réessayer plus tard!",
    it: 'Qualcosa è andato storto nei nostri collegamenti interni! Riprova più tardi!'
  },
  NonceTooOld: {
    en: 'Nonce too old. Please try logging in again!',
    fr: 'Nonce trop vieux. Veuillez vous reconnecter!',
    it: 'Nonce troppo vecchio. Riprova a effettuare il login!'
  },
  BadExchange: {
    en: 'Something went wrong while we tried to log you in!',
    fr: "Quelque chose s'est mal passé lors de la connexion!",
    it: 'Qualcosa è andato storto durante il login!'
  },
  BadExchangeJson: {
    en: 'Something went wrong while we tried to log you in! Could be due to discord bugging out?',
    fr: "Quelque chose s'est mal passé lors de la connexion! Peut-être due à discord buggant?",
    it: 'Qualcosa è andato storto durante il login! Potrebbe essere dovuto a discord buggando?'
  },
  NoUser: {
    en: 'Could not find a user with that ID! Something serious just happened on our end! Contact support.',
    fr: "Impossible de trouver un utilisateur avec cet ID! Quelque chose s'est mal passé sur notre côté! Contactez le support.",
    it: 'Impossibile trovare un utente con questo ID! Qualcosa è andato storto sul nostro lato! Contatta il supporto.'
  },
  'CheckBotError.AlreadyExists': {
    en: 'This bot already exists on Fates List',
    fr: 'Ce bot existe déjà sur Fates List',
    it: 'Questo bot esiste già su Fates List'
  },
  'CheckBotError.ClientIDImmutable': {
    en: 'Client ID cannot be changed once set',
    fr: "L'ID client ne peut pas être modifié une fois défini",
    it: "L'ID client non può essere modificato una volta impostato"
  },
  'CheckBotError.PrefixTooLong': {
    en: 'Prefix must be shorter than 9 characters',
    fr: 'Le préfix doit être plus court que 9 caractères',
    it: 'Il prefisso deve essere più corto di 9 caratteri'
  },
  'CheckBotError.NoVanity': {
    en: "You must have a vanity for your bot. This can be your username. You can prefix it with _ (underscore) if you don't want the extra growth from it. For example _mewbot would disable the mewbot vanity",
    fr: "Vous devez avoir un vanity pour votre bot. Cela peut être votre pseudo. Vous pouvez le préfixer avec _ (underscore) si vous ne voulez pas l'extra-croissance de celui-ci. Par exemple _mewbot désactiverai le vanity mewbot",
    it: "Devi avere un vanity per il tuo bot. Questo può essere il tuo username. Puoi prefissarlo con _ (underscore) se non vuoi l'extra-crescita di quello. Per esempio _mewbot disattiverà il vanity mewbot"
  },
  'CheckBotError.VanityTaken': {
    en: 'This vanity has already been taken. Please contact Fates List staff if you wish to report this!',
    fr: 'Ce vanity a déjà été pris. Contactez le staff de Fates List si vous souhaitez signaler ceci!',
    it: 'Questo vanity è già stato preso. Contatta il staff di Fates List se vuoi segnalare questo!'
  },
  'CheckBotError.InvalidInvitePermNum': {
    en: 'This invites permissions are invalid!',
    fr: "Ces permissions d'invitation sont invalides!",
    it: 'Queste autorizzazioni per gli inviti sono invalide!'
  },
  'CheckBotError.InvalidInvite': {
    en: 'Your invite link must start with https://',
    fr: "Votre lien d'invitation doit commencer par https://",
    it: 'Il tuo link di invito deve iniziare con https://'
  },
  'CheckBotError.ShortDescLengthErr': {
    en: 'Your description must be at least 10 characters long and must be a maximum of 200 characters',
    fr: "Votre description doit être d'au moins 10 caractères et ne doit pas dépasser 200 caractères",
    it: 'La tua descrizione deve essere di almeno 10 caratteri e non può superare i 200 caratteri'
  },
  'CheckBotError.LongDescLengthErr': {
    en: 'Your long description must be at least 200 characters long',
    fr: "Votre description longue doit être d'au moins 200 caractères",
    it: 'La tua descrizione lunga deve essere di almeno 200 caratteri'
  },
  'CheckBotError.BotNotFound': {
    en: "According to Discord's API and our cache, your bot does not exist. Please try again after 2 hours.",
    fr: "Selon l'API de Discord et notre cache, votre bot n'existe pas. Veuillez réessayer après 2 heures.",
    it: "In base all'API di Discord e al nostro cache, il tuo bot non esiste. Riprova dopo 2 ore."
  },
  'CheckBotError.NoTags': {
    en: 'You must select tags for your bot',
    fr: 'Vous devez sélectionner des tags pour votre bot',
    it: 'Devi selezionare i tag per il tuo bot'
  },
  'CheckBotError.TooManyTags': {
    en: 'You can only select up to 10 tags for your bot',
    fr: 'Vous ne pouvez sélectionner un maximum de 10 tags pour votre bot',
    it: 'Puoi selezionare un massimo di 10 tag per il tuo bot'
  },
  'CheckBotError.TooManyFeatures': {
    en: 'You can only select up to 5 features for your bot',
    fr: "Vous ne pouvez sélectionner qu'un maximum de 5 fonctionnalités pour votre bot",
    it: 'Puoi selezionare un massimo di 5 funzioni per il tuo bot'
  },
  'CheckBotError.EditLocked': {
    en: 'This bot has either been locked by staff or has been edit locked by the main owner of the bot',
    fr: 'Ce bot a été bloqué par le staff ou a été bloqué par le propriétaire principal du bot',
    it: 'Questo bot è stato bloccato da staff o è stato bloccato da il proprietario principale del bot'
  },
  'CheckBotError.OwnerListTooLong': {
    en: 'The owner list is too long. You may only have a maximum of 5 extra owners',
    fr: 'La liste des propriétaires est trop longue. Vous ne pouvez avoir un maximum de 5 propriétaires supplémentaires',
    it: 'La lista dei proprietari è troppo lunga. Puoi avere un massimo di 5 proprietari extra'
  },
  'CheckBotError.ClientIDNeeded': {
    en: 'Client ID is required for this bot or is incorrect',
    fr: "L'ID client est requis pour ce bot ou est incorrect",
    it: "L'ID client è necessario per questo bot o è incorretto"
  },
  'CheckBotError.InvalidClientID': {
    en: 'Client ID inputted is invalid for this bot',
    fr: "L'ID client entré est invalide pour ce bot",
    it: "L'ID client inserito è invalido per questo bot"
  },
  'CheckBotError.PrivateBot': {
    en: 'This bot is private and cannot be added to Fates List',
    fr: 'Ce bot est privé et ne peut pas être ajouté à Fates List',
    it: 'Questo bot è privato e non può essere aggiunto a Fates List'
  },
  'CheckBotError.OwnerIDParseError': {
    en: 'An owner ID in your owner list is invalid (hint: not a snowflake)',
    fr: 'Un ID de propriétaire dans votre liste est invalide (indice: pas un snowflake)',
    it: 'Un ID di proprietario nella tua lista è invalido (indice: non è un snowflake)'
  },
  'CheckBotError.OwnerNotFound': {
    en: 'An owner ID in your owner list does not exist',
    fr: "Un ID de propriétaire dans votre liste n'existe pas",
    it: 'Un ID di proprietario nella tua lista non esiste'
  },
  'CheckBotError.MainOwnerAddAttempt': {
    en: 'You cannot add a main owner as an extra owner',
    fr: 'Vous ne pouvez pas ajouter un propriétaire principal comme propriétaire supplémentaire',
    it: 'Non puoi aggiungere un proprietario principale come proprietario extra'
  },
  'CheckBotError.ExtraLinkKeyTooLong': {
    en: 'One of your extra link keys is too long',
    fr: 'Une de vos clés de lien supplémentaire est trop longue',
    it: 'Uno dei tuoi link extra è troppo lungo'
  },
  'CheckBotError.ExtraLinkValueTooLong': {
    en: 'One of your extra link values is too long',
    fr: 'Une de vos valeurs de lien supplémentaire est trop longue',
    it: 'Uno dei tuoi link extra è troppo lungo'
  },
  'CheckBotError.ExtraLinkValueNotHTTPS': {
    en: 'One of your extra link values is not a valid URL (hint: check that its HTTPS and not HTTP)',
    fr: "Une de vos valeurs de lien supplémentaire n'est pas une URL valide (indice: vérifiez qu'il s'agit d'un HTTPS et non d'un HTTP)"
  },
  'CheckBotError.ExtraLinksTooManyRendered': {
    en: 'You have too many renderable extra links (extra links that do not start with an underscore)',
    fr: 'Vous avez trop de liens supplémentaires rendus (liens supplémentaires qui ne commencent pas par un underscore)',
    it: 'Hai troppi link extra renderizzabili (link extra che non iniziano con un underscore)'
  },
  'CheckBotError.ExtraLinksTooMany': {
    en: 'You have too many extra links. Try removing some?',
    fr: 'Vous avez trop de liens supplémentaires. Essayez de les enlever?',
    it: 'Hai troppi link extra. Prova a rimuoverne uno?'
  },
  'CheckBotError.BannerPageError': {
    en: 'An error occurred while fetching the banner page for validation...',
    fr: 'Une erreur est survenue lors de la récupération de la page de bannière pour validation...',
    it: 'Si è verificato un errore durante il recupero della pagina banner per la validazione...'
  },
  'CheckBotError.BannerCardError': {
    en: 'An error occurred while fetching the banner card for validation...',
    fr: 'Une erreur est survenue lors de la récupération de la carte de bannière pour validation...',
    it: 'Si è verificato un errore durante il recupero della carta banner per la validazione...'
  },
  'CheckBotError.JAPIError': {
    en: 'An error occurred while our anti-abuse provider handled your bot...',
    fr: "Une erreur est survenue lors du traitement de votre bot par notre systeme d'anti-abus...",
    it: 'Si è verificato un errore durante il gestito dal nostro sistema anti-abuso...'
  },
  'CheckBotError.JAPIDeserError': {
    en: 'An error occurred while our anti-abuse provider handled your bot...',
    fr: "Une erreur est survenue lors du traitement de votre bot par notre systeme d'anti-abus...",
    it: 'Si è verificato un errore durante il gestito dal nostro sistema anti-abuso...'
  },
  'CheckBotError.NotMainOwner': {
    en: 'This action needs you to be the main owner of this bot!'
  },
  InvalidFlag: {
    en: 'Illegal or otherwise non-edittable flag set on this profile',
    fr: 'Le flag est illégal ou non éditable',
    it: 'Il flag è illegale o non editabile'
  },
  'VoteBotError.Wait': {
    en: "You've already voted recently!",
    fr: 'Vous avez déjà voté récemment!',
    it: 'Hai già votato recentemente!'
  },
  'VoteBotError.UnknownError': {
    en: 'An unknown error occurred. Please ask for help on the Fates List support server.',
    fr: "Une erreur inconnue est survenue. Veuillez demander de l'aide sur le serveur de support Fates List.",
    it: 'Si è verificato un errore sconosciuto. Chiedi aiuto sul server di supporto Fates List.'
  },
  'VoteBotError.System': {
    en: 'This is a system bot or server and as such cannot be voted for at this time',
    fr: 'Ceci est un bot système ou serveur et ne peut pas être voté pour pour le moment',
    it: 'Questo è un bot o server di sistema quindi non può essere votato per il momento'
  },
  'VoteBotError.AutoroleError': {
    en: 'For some odd reason, we have failed to give you autoroles for voting for this server. Are you on this server?',
    fr: "Pour une raison inconnue, nous n'avons pas pu vous attribuer des rôles automatiquement lors de votre vote pour ce serveur. Êtes-vous sur ce serveur?",
    it: 'Per qualche motivo, non siamo riusciti a darti i ruoli automatici per votare per questo server. Sei su questo server?'
  },
  ExpNotEnabled: {
    en: "Whoa there! You aren't whitelisted to access this top-secret experiment yet!",
    fr: "Whoa! Vous n'êtes pas autorisé à accéder à cet expérimentation secrète pour le moment!",
    it: 'Whoa! Non sei autorizzato ad accedere a questo sperimento segreto per il momento!'
  },
  CommandLengthError: {
    en: 'This command is too long! Please try a shorter command name and/or description',
    fr: 'Cette commande est trop longue! Veuillez essayer un nom de commande et/ou une description plus courte',
    it: 'Questo comando è troppo lungo! Prova un comando più corto e/o una descrizione più corta'
  },
  StarRatingOutOfRange: {
    en: 'Star rating must be between 1 to 10. How did <em>this</em> happen?',
    fr: "Le nombre d'étoiles doit être compris entre 1 et 10. Comment <em>ceci</em> est arrivé?",
    it: 'Il voto deve essere compreso tra 1 e 10. Come è capitato <em>questo</em>?'
  },
  ReviewTextError: {
    en: 'Review text must be between 10 and 20000 characters long!',
    fr: 'Le texte de la critique doit être compris entre 10 et 20000 caractères!',
    it: 'Il testo della recensione deve essere compreso tra 10 e 20000 caratteri!'
  },
  ReviewAlreadyExists: {
    en: 'You have already made a review for this bot. Please edit that instead!',
    fr: 'Vous avez déjà fait une critique pour ce bot. Veuillez la modifier à la place!',
    it: 'Hai già fatto una recensione per questo bot. Modificala invece!'
  },
  ParentReviewInvalid: {
    en: 'The parent ID you are trying to reply to is invalid. How did <em>this</em> happen?',
    fr: "L'ID du parent que vous essayez de répondre est invalide. Comment <em>ceci</em> est arrivé?",
    it: "L'ID del parent che stai cercando di rispondere non è valido. Come è capitato <em>questo</em>?"
  },
  ReviewAlreadyVoted: {
    en: 'You have already voted for this review! Please change that instead?',
    fr: 'Vous avez déjà voté pour cette critique! Veuillez la changer à la place?',
    it: 'Hai già votato per questa recensione! Modificala invece?'
  },
  'Appeal.TextError': {
    en: 'Appeal length must be between 7 and 4000 characters long!'
  },
  'Appeal.BotNotApproved': {
    en: 'You cannot certify a bot/server that is not approved yet!'
  },
  'Appeal.NoBannerCard': {
    en: "You cannot certify a bot/server that has no banner for the bot card set yet! You can set one under 'Extras'"
  },
  'Appeal.NoBannerPage': {
    en: "You cannot certify a bot/server that has no banner for the bots page set yet! You can set one under 'Extras'"
  },
  'Appeal.TooFewGuilds': {
    en: 'You cannot certify a bot that is in less than 100 guilds!'
  },
  'Appeal.TooFewMembers': {
    en: 'You cannot certify a server that has less than 100 members!'
  },
  APIBan: {
    en: 'You have been banned from using this API endpoint!'
  },
  BadStats: {
    en: "Whoa there! You've got some nerve trying to post invalid stats to us!"
  },
  JAPIError: {
    en: 'Our anti-abuse provider seems to have had an issue this morning!'
  },
  JAPIDeserError: {
    en: 'Our anti-abuse provider comm-links seems to have had an issue this morning!'
  },
  ClientIDNeeded: {
    en: 'You need to set a client ID in Bot Settings to use this endpoint!'
  },
  TooManySubscriptions: {
    en: 'You have too many push notifications set up already! Please delete some before trying again!'
  },
  'PackCheckError.TooManyBots': {
    en: 'This pack has too many bots!'
  },
  'PackCheckError.InvalidBotId': {
    en: 'This pack has an invalid bot ID!'
  },
  'PackCheckError.TooFewBots': {
    en: 'This pack has too few bots!'
  },
  'PackCheckError.InvalidIcon': {
    en: 'This pack has an invalid icon URL!'
  },
  'PackCheckError.InvalidBanner': {
    en: 'This pack has an invalid banner URL!'
  },
  'PackCheckError.InvalidPackId': {
    en: 'This pack has an invalid ID! Contact Fates List staff if you see this!'
  },
  'PackCheckError.DescriptionTooShort': {
    en: "This pack's description is too short!"
  },
  JsonContext: {
    en: 'This error is caused by a malformed JSON object. Please contact Fates List staff if you see this as this is a bug!'
  }
};

export function getIntlString(key: string, lang = 'en'): string {
  if (translations[key] && translations[key][lang]) {
    return translations[key][lang];
  } else if (translations[key] && translations[key]['en']) {
    return translations[key]['en'];
  } else {
    if (key.startsWith('Json ')) {
      key += '<br/><br/>' + getIntlString('JsonContext', lang);
    }
    return key;
  }
}

export function genError(json): string {
  return getIntlString(json.reason) + '<br/><br/>' + (json.context || '');
}
