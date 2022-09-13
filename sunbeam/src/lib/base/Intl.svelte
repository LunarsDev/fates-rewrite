<script lang="ts">
  import { page } from '$app/stores';
  import { getIntlString } from '$lib/strings';

  export let key: string;

  let lang = 'en';

  if ($page.data.user) {
    lang = $page.data.site_lang;
  }

  if (!lang) {
    lang = 'en';
  }
</script>

{getIntlString(key, lang)}
