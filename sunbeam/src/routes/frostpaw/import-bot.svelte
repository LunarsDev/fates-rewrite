<script lang="ts" context="module">
  import { fetchFates } from '$lib/request';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    if (!session.session.token) {
      return {
        props: {
          sources: {}
        }
      };
    }
    let importSrcRes = await fetchFates('/import-sources', '', fetch, false, true);
    if (!importSrcRes.ok) {
      return {
        status: importSrcRes.status,
        error: new Error('Could not fetch import source list')
      };
    }
    let data = await importSrcRes.json();
    return {
      props: {
        sources: data
      }
    };
  }
</script>

<script lang="ts">
  import { browser } from '$app/env';
  import BotSettings from '$lib/pages/BotSettings.svelte';
  import { loginUser } from '$lib/request';
  import { session } from '$app/stores';
  import { apiUrl } from '$lib/config';
  import Tip from '$lib/base/Tip.svelte';
  import FormInput from '$lib/base/FormInput.svelte';
  import Button from '$lib/base/Button.svelte';
  import navigationState from '$lib/navigationState';
  import alertstore from '$lib/alertstore';
  import loadstore from '$lib/loadstore';
  import { genError } from '$lib/strings';
  import { enums } from '$lib/enums/enums';
  export let sources: any;
  if (!$session.session.token) {
    if (browser) {
      loginUser(false);
    }
  }

  let popUpMsg = 'Errors will appear here (just in case you have popups disabled)';

  function popup(msg: string, title = 'Error') {
    popUpMsg = msg;
    saveTxt = 'Import';
    alert({
      title: title,
      message: msg,
      id: 'error',
      type: enums.AlertType.Error
    });
  }

  let saveTxt = 'Import';

  let importWarnSent = false;
  let extData = {};

  async function importBot() {
    saveTxt = `${saveTxt}ing`;
    $loadstore = 'Importing...';
    $navigationState = 'loading';

    let botId = (document.querySelector('#bot_id') as HTMLInputElement).value;
    let source = (document.querySelector('#source') as HTMLInputElement).value;

    if (!botId) {
      popup('Please enter a bot ID', 'Whoa there!');
      return;
    }

    let extQuery = '';

    if (source == 'Custom') {
      // Custom import source
      let importURL = (document.querySelector('#import-url') as HTMLInputElement).value;
      if (!importURL.startsWith('https://')) {
        popup('Custom import source must be a valid URL', 'Whoa there!');
        return;
      }

      if (!importURL.includes('/api/') && !importWarnSent) {
        importWarnSent = true;
        popup(
          "This does not appear to be a proper API. Click 'Import' again if you're sure this is a proper API URL",
          'Whoa there!'
        );
        return;
      }

      let data;

      try {
        data = await fetch(importURL, {
          headers: {
            Authorization: (document.querySelector('#api-token') as HTMLInputElement).value
          }
        });
      } catch (err) {
        popup(`Could not connect to API: ${err}`, 'Whoa there!');
        return;
      }

      if (data.status == 401) {
        popup('Invalid API token? Import source returned 401', 'Whoa there!');
        return;
      } else if (!data.ok) {
        popup('Invalid URL? Import source returned an error', 'Whoa there!');
        return;
      }

      extData = await data.json();

      if (!extData['owners']) {
        if (extData['additional_owners']) {
          extData['owners'] = extData['additional_owners'];
        } else {
          extData['owners'] = [$session.session.user.id];
        }
      }
      if (!extData['description']) {
        // Attempt to find data
        if (extData['shortdesc']) {
          extData['description'] = extData['shortdesc'];
        } else if (extData['desc']) {
          extData['description'] = extData['desc'];
        } else {
          // Last resort to try
          let key = Object.keys(extData).filter((k) => k.includes('desc') && !k.includes('long'));
          if (key.length > 0) {
            extData['description'] = extData[key[0]];
          } else {
            popup("Seems like this source doesn't provide a proper description", 'Whoa there!');
            return;
          }
        }
      }

      if (!extData['long_description']) {
        if (extData['longdesc']) {
          extData['long_description'] = extData['longdesc'];
        } else {
          // Last resort to try
          let key = Object.keys(extData).filter((k) => k.includes('desc') && k.includes('long'));
          if (key.length > 0) {
            extData['long_description'] = extData[key[0]];
          } else {
            popup(
              "Seems like this source doesn't provide a proper long description",
              'Whoa there!'
            );
            return;
          }
        }
      }

      extQuery = `&custom_source=${importURL.replace('https://', '').split('/')[0]}`;
    }

    let res = await fetch(
      `${apiUrl}/users/${$session.session.user.id}/bots/${botId}/import?src=${source}${extQuery}`,
      {
        method: 'POST',
        headers: {
          Authorization: $session.session.token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ext_data: extData })
      }
    );

    if (res.ok) {
      $loadstore = '';
      alert({
        title: 'Success',
        message: 'Bot imported successfully',
        id: 'success',
        type: enums.AlertType.Success
      });
    } else {
      let json = await res.json();
      popup(genError(json));
    }
  }

  function topggAutofill() {
    let botId = (document.querySelector('#bot_id') as HTMLInputElement).value;
    (
      document.querySelector('#import-url') as HTMLInputElement
    ).value = `https://top.gg/api/bots/${botId}`;
    popup(
      "Autofill done, now specify a top.gg API token under the API token column and you'll be ready to go!",
      'Success'
    );
  }

  let source: string;
</script>

{#if $session.session.token}
  <h1 class="text-center">Import A Bot!</h1>
  <div id="source-view">
    <Tip>
      This feature is still in beta!<br /><br />

      As this feature evolves, more bot lists to import from may be added!<br /><br />

      All listed bot lists have given their express permission to be added to this system.
      Furthermore, by continuing, you confirm that you are the owner of the bot in question.<br
      /><br />

      All bot lists/import sources can request to be blacklisted from this feature and we will do so
      immediately. However as bot owners are the creator of the bot in question, we believe this to
      be fair use with permission to access the bot provided by the bots owners (who are the content
      creators). <br /><br />

      Servers cannot and will never be importable due to privacy concerns<br /><br />
    </Tip>
    <label for="source">Import Source</label>
    <select name="source" id="source" bind:value={source}>
      {#each sources.sources as source}
        <option value={source.id}>{source.name}</option>
      {/each}
    </select>
    <FormInput
      name="Bot ID (must be bot owner)"
      id="bot_id"
      type="number"
      placeholder="Bot ID here"
    />
    {#if source == 'Custom'}
      <Tip>
        You can always contact us over DMs if you wish to blacklist a URL from being imported to for
        any reason.<br /><br />

        This feature is provided so bot developers can easily add their bot to Fates List. It
        requires their explicit knowledge and permission.<br /><br />

        Most (good) bot lists will have a API you can directly specify for import URL and many also
        support CORS. Examples:<br /><br />

        <ul>
          <li>
            <a href="https://docs.top.gg">https://docs.top.gg</a> (yet another good bot list for discord)
            [Import URL: https://top.gg/api/bots/BOT_ID_HERE with API Token of your bots token]
          </li>
        </ul>
      </Tip>
      <Button onclick={topggAutofill}  class="button btn-save"
        >Import from top.gg</Button
      >
      <FormInput
        name="Import URL"
        id="import-url"
        type="text"
        placeholder="URL to import your bot from"
      />
      <FormInput
        name="API token for import (if required)"
        id="api-token"
        type="text"
        placeholder="API token (if the source you use requires this, many do)"
      />
      <Tip>
        This is only shared with the import source in question and is not stored on Fates List.<br
        /><br />

        Due to this being fully client side, the source you specify here must support CORS (you can
        disable CORS in a temporary browsing session using <code>--disable-web-security</code> on chrome
        etc. but this is highly not recommended). If you do not know whether or not your source supports
        CORS or not, then just try and see if it errors.
      </Tip>
    {/if}
    <Button onclick={() => importBot()}  class="button btn-save">{saveTxt}</Button
    >
    <pre>Recieved data (for debugging): {JSON.stringify(extData)}</pre>
    <pre>{popUpMsg}</pre>
  </div>
{:else}
  <p>Logging you in, please wait...</p>
{/if}

<style>
  #source-view {
    margin-left: 30px;
    margin-right: 30px;
  }
</style>
