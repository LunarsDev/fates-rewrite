<script lang="ts">
  import { session } from '$app/stores';
  import { getIntlString } from '$lib/strings';

  export let key: string;

  let lang = 'en';

  if ($session.session.user) {
    lang = $session.session.site_lang;
  }

  if (!lang) {
    lang = 'en';
  }
</script>

{getIntlString(key, lang)}
