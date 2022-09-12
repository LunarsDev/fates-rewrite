<script lang="ts" context="module">
  import { fetchFates } from '$lib/request';
  import { enums } from '$lib/enums/enums';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    // Check perms
    if (!session.session.token || session.session.user.id != params.id) {
      return {
        status: 403,
        error: new Error('Forbidden')
      };
    }

    // Get profile
    let url = `/profiles/${params.id}`;
    const res = await fetchFates(url, '', fetch, false, true);
    if (res.ok) {
      let data = await res.json();

      return {
        props: {
          data: data
        }
      };
    }

    return {
      status: res.status,
      error: new Error(`Profile Not Found`)
    };
  }
</script>

<script lang="ts">
  import Tab from '$lib/base/Tab.svelte';
  import { page, session } from '$app/stores';
  import SelectOption from '$lib/base/SelectOption.svelte';
  import Button from '$lib/base/Button.svelte';
  import Tip from '$lib/base/Tip.svelte';
  import BotPack from '$lib/base/BotPack.svelte';
  import { apiUrl, nextUrl } from '$lib/config';
  import AuditLogs from '$lib/base/AuditLogs.svelte';
  import Checkbox from '$lib/base/Checkbox.svelte';
  import alertstore from '$lib/alertstore';
  import navigationState from '$lib/navigationState';
  import { genError } from '$lib/strings';
  import * as logger from '$lib/logger';

  let popUpMsg = 'Errors will appear here (just in case you have popups disabled)';

  function popup(msg: string, title = 'Error') {
    popUpMsg = msg;
    alert({
      title: title,
      message: msg,
      show: true,
      id: 'error',
      type: enums.AlertType.Error
    });
  }

  export let data: any;

  let tabs = [
    {
      name: 'About',
      id: 'about'
    },
    {
      name: 'Actions',
      id: 'actions'
    },
    {
      name: 'Basics',
      id: 'basics'
    },
    {
      name: 'CSS',
      id: 'css'
    }
  ];

  let firstTimeShowedWarning = false; // Whether or not we have sent the warning alert once or not

  let userToken =
    "Hidden, click 'Show' to show it and make sure to NEVER share it with anyone else";

  function showUserToken() {
    let b = document.querySelector('#user-token-show-btn');
    if (!firstTimeShowedWarning) {
      userToken = $session.session.token;
      popup('Warning: Do not share this with anyone', 'Important');
      firstTimeShowedWarning = true;
      b.textContent = 'Hide';
      return;
    }
    if (b.textContent == 'Show') {
      userToken = $session.session.token;
      b.textContent = 'Hide';
    } else {
      userToken = 'Hidden';
      b.textContent = 'Show';
    }
  }

  async function regenUserToken() {
    let url = `${nextUrl}/users/${data.user.id}/token`;
    let headers = { Authorization: `User ${$session.session.token}` };
    let res = await fetch(url, {
      method: 'DELETE',
      headers: headers
    });
    if (res.ok) {
      popup('Regenerated token, you will need to login again', 'Important');
      fetch(`${nextUrl}/oauth2`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          Frostpaw: '0.1.0'
        }
      })
        .then((res) => res.json())
        .then((json) => {
          window.location.reload(); // Only place its really needed
        });
    } else {
      popup(`Error during token regeneration: ${res.status}`);
    }
  }

  async function updateProfile() {
    let flags = [];
    if (data.user_experiments.includes(enums.UserExperiments.VotePrivacy)) {
      if ((document.querySelector('#vote-privacy') as HTMLInputElement).checked) {
        flags.push(enums.UserFlags.VotesPrivate);
      }
    }
    let payload = {
      flags: flags,
      user_experiments: [],
      description: (document.querySelector('#description') as HTMLInputElement).value,
      description_raw: '', // Uneeded by API
      profile_css: (document.querySelector('#profile-css') as HTMLInputElement).value,
      user_css: (document.querySelector('#user-css') as HTMLInputElement).value,
      site_lang: (document.querySelector('#site-lang') as HTMLInputElement).value,
      vote_reminder_channel: (document.querySelector('#vote-reminder-channel') as HTMLInputElement)
        .value,
      packs: [],
      bots: [],
      action_logs: [],
      connections: [],
      state: 0,
      user: {
        id: data.user.id,
        username: '',
        disc: '',
        avatar: '',
        status: 'Unknown',
        bot: false
      },
      extra_links: {} // TODO: Add support for this directly to sunbeam
    };
    logger.info('ProfileSettings', 'New settings object is: ', JSON.stringify(payload));
    let url = `${nextUrl}/profiles/${data.user.id}`;
    let headers = { Authorization: $session.session.token, 'Content-Type': 'application/json' };
    let res = await fetch(url, {
      method: 'PATCH',
      headers: headers,
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      popup('Updated your profile successfully', 'Success');
    } else {
      let json = await res.json();
      popup(genError(json));
    }
  }

  async function addBotPack() {
    let payload = {
      id: '',
      name: (document.querySelector('#pack-name') as HTMLInputElement).value,
      description: (document.querySelector('#pack-desc') as HTMLInputElement).value,
      icon: (document.querySelector('#pack-icon') as HTMLInputElement).value,
      banner: (document.querySelector('#pack-banner') as HTMLInputElement).value,
      owner: {
        id: data.user.id,
        username: '',
        avatar: '',
        disc: '',
        status: 'Unknown',
        bot: false
      },
      created_at: '1970-01-01T00:00:00Z'
    };
    let bots = (document.querySelector('#pack-bots') as HTMLInputElement).value;
    payload['resolved_bots'] = bots
      .replace(' ', '')
      .split(',')
      .map((el) => {
        return {
          user: {
            id: el,
            username: '',
            avatar: '',
            disc: '',
            status: 'Unknown',
            bot: true
          },
          description: ''
        };
      });
    let headers = { Authorization: $session.session.token, 'Content-Type': 'application/json' };
    let res = await fetch(`${nextUrl}/users/${data.user.id}/packs`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      popup('Added pack successfully', 'Success');
      return;
    } else {
      let json = await res.json();
      popup(genError(json));
    }
  }

  async function delBotPack(packId: string) {
    if (!packId) {
      popup('No Pack ID given');
      return;
    }
    let headers = { Authorization: $session.session.token };
    let res = await fetch(`${nextUrl}/users/${data.user.id}/packs/${packId}`, {
      method: 'DELETE',
      headers: headers
    });
    if (res.ok) {
      popup('Deleted pack successfully', 'Success');
      return;
    } else {
      let json = await res.json();
      popup(genError(json));
    }
  }

  async function revokeClient(cliId) {
    let headers = { Authorization: $session.session.token };
    let res = await fetch(`${nextUrl}/users/${data.user.id}/frostpaw/clients/${cliId}`, {
      method: 'DELETE',
      headers: headers
    });
    if (res.ok) {
      popup('Revoked client successfully', 'Success');
      return;
    } else {
      let json = await res.json();
      popup(genError(json));
    }
  }

  async function getOldRoles() {
    let url = `${nextUrl}/profiles/${data.user.id}/old-roles`;
    let headers = { Authorization: $session.session.token };
    let res = await fetch(url, {
      method: 'PUT',
      headers: headers
    });
    if (res.ok) {
      let json = await res.json();

      let roles = [];

      if (json.bot_developer) {
        roles.push('Bot Developer');
      }
      if (json.certified_developer) {
        roles.push('Certified Developer');
      }

      let rolesList = document.querySelector('#new-roles') as HTMLUListElement;
      rolesList.innerHTML = 'Roles gotten';
      roles.forEach((role) => {
        let li = document.createElement('li');
        li.textContent = role;
        rolesList.appendChild(li);
      });

      document.querySelector('#gor-btn').remove();
    } else {
      let json = await res.json();
      popup(genError(json));
    }
  }

  // Sigh svelte
  let placeholderUserCss =
    'Warning: Fates List is not responsible for any issues due to your custom user CSS. To use javascript in custom css, put your JS in a LT/styleGTLTscriptGTYOUR JS HERELT/scriptGTLTstyleGT tag';

  let roles;

  function getDelPackIdEl(): HTMLInputElement {
    return document.querySelector('#del-pack-id');
  }
</script>

<img
  class="user-avatar"
  loading="lazy"
  src={data.user.avatar.replace('.png', '.webp').replace('width=', 'width=120px')}
  id="user-avatar"
  alt="{data.user.username}'s avatar"
  on:error={function () {
    this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
  }}
/>
<h1 class="white user-username" id="user-name">{data.user.username}</h1>
<h2 id="user-description">Profile Settings</h2>
<Tab tabs={tabs} defaultTabButton="about-tab-button">
  <section id="about-tab" class="tabcontent tabdesign">
    <h2>User Token</h2>
    <p class="white">
      <em>Accidentally</em> leaked your API token? Just be sure to change the token everywhere you use
      it and make sure it doesn't happen again!
    </p>
    <pre id="user-token-field">{userToken}</pre>
    <Button
      href={'#'}
      onclick={showUserToken}
      class="button"
      id="user-token-show-btn"
      touch
      >Show</Button
    >
    <Button
      href={'#'}
      onclick={regenUserToken}
      class="button"
      id="user-token-regen-btn"
      touch
      >Regenerate</Button
    >

    <h2>Connections</h2>
    {#each data.connections as conn}
      <div class="connection-container">
        <h3>{conn.client.name}</h3>
        <p>
          The last refresh token for this client after which you will need to reauthorize expires at {conn.expires_on}
        </p>
        <p>You have authorized this client {conn.repeats} times!</p>
        <ul>
          <li>Client ID: <span class="opaque">{conn.client.id}</span></li>
          <li>Client Owner: <span class="opaque">{conn.client.owner.username}</span></li>
          <li>Client Owner ID: <span class="opaque">{conn.client.owner.id}</span></li>
        </ul>
        <Button
          href={'#'}
          onclick={() => {
            revokeClient(conn.client.id);
          }}
          class="button"
          id="danger-revoke-btn-{conn.client.id}"
          style="background-color: red"
          touch
          >Revoke</Button
        >
      </div>
    {/each}
    {#if data.connections.length === 0}
      <p class="white">You're all set! You have no connections with any custom clients.</p>
    {/if}

    <h2>Get Old Roles</h2>
    <p>
      Just joined our support server and need to get your roles (Bot Developer, Certified
      Developer). Click here
    </p>
    <div id="new-roles" />
    <Button href={'#'} onclick={getOldRoles} class="button" id="gor-btn" 
      >Get Old Roles</Button
    >

    <h2>Your Packs</h2>
    {#each data.packs as pack}
      <p>Pack ID: <span class="opaque">{pack.id}</span></p>
      <BotPack pack={pack} centered={false} />
      <Button
        href={'#'}
        onclick={() => {
          delBotPack(pack.id);
        }}
        class="button"
        id="del-bot-pack-btn"
        touch
        >Delete {pack.name}</Button
      >
    {/each}
    <h2>Profile Info</h2>
    <p>Profile State: {enums.UserState[data.state]} ({data.state})</p>
    <AuditLogs logs={data.action_logs} />
    <h2>User Experiments</h2>
    <p>Don't worry about this if you don't know what it is!</p>
    <ul>
      {#each data.user_experiments as exp}
        <li>{enums.UserExperiments[exp] || enums.UserExperiments[0]} ({exp})</li>
      {/each}
    </ul>
  </section>
  <section id="actions-tab" class="tabcontent tabdesign">
    <h2>Create Bot Packs</h2>
    <Tip>Bot Packs are a way of grouping bots into one package!</Tip>
    <label for="pack-name">Pack Name</label>
    <input id="pack-name" name="pack-name" class="fform" placeholder="Name it something snazzy!" />
    <label for="pack-desc">Pack Description</label>
    <input id="pack-desc" name="pack-desc" class="fform" placeholder="What does this pack do?" />
    <label for="pack-icon">Pack Icon</label>
    <input
      id="pack-icon"
      name="pack-icon"
      class="fform"
      placeholder="{apiUrl}/static/botlisticon.webp etc."
    />
    <label for="pack-banner">Pack Banner</label>
    <input
      id="pack-banner"
      name="pack-banner"
      class="fform"
      placeholder="{apiUrl}/static/botlisticon.webp etc."
    />
    <label for="pack-bots">Bots (comma seperated)</label>
    <input id="pack-bots" name="pack-bots" class="fform" placeholder="10293,29392,39492 etc." />
    <Button
      href={'#'}
      onclick={addBotPack}
      class="button"
      id="add-bot-pack-btn"
      touch
      >Add Pack</Button
    >

    <h2>Delete Bot Packs</h2>
    <Tip>You can get a bot pack's ID from the Bot Pack List under About or by using our API</Tip>
    <label for="del-pack-id">Pack ID</label>
    <input
      id="del-pack-id"
      name="del-pack-id"
      class="fform"
      placeholder="df3b4053-eaed-45d6-9e26-470be52cd80c etc."
    />
    <Button
      href={'#'}
      onclick={() => {
        let packId = getDelPackIdEl().value;
        delBotPack(packId);
      }}
      class="button"
      id="del-bot-pack-btn"
      touch
      >Delete Pack</Button
    >
  </section>
  <section id="basics-tab" class="tabcontent tabdesign">
    <label for="site-lang">Site Language</label>
    <select name="site-lang" id="site-lang">
      <SelectOption value="en" masterValue={data.site_lang}>English</SelectOption>
      <SelectOption value="es" masterValue={data.site_lang}>Spanish</SelectOption>
      <SelectOption value="fr" masterValue={data.site_lang}>French</SelectOption>
      <SelectOption value="hi" masterValue={data.site_lang}>Hindi</SelectOption>
      <SelectOption value="ru" masterValue={data.site_lang}>Russian</SelectOption>
    </select>
    {#if data.user_experiments.includes(enums.UserExperiments.VotePrivacy)}
      <Checkbox id="vote-privacy" data={data.flags.includes(enums.UserFlags.VotesPrivate)}
        >Hide votes to other users</Checkbox
      >
    {/if}
    <label for="vote-reminder-channel"
      >Vote Reminders Channel (set using /vrchannel in Squirrelflight)</label
    >
    <input
      name="vote-reminder-channel"
      id="vote-reminder-channel"
      class="fform"
      placeholder="Set using vrchannel command in Squirrelflight"
      disabled
      tabindex="-1"
      value={data.vote_reminder_channel}
      style="width: 100%"
    />
    <label for="description">Description</label>
    <textarea
      name="description"
      id="description"
      class="form-control fform text-input"
      style="width: 100%"
      placeholder="Enter a description for your profile here">{data.description_raw}</textarea
    >
  </section>
  <section id="actions-tab" class="tabcontent tabdesign" />
  <section id="css-tab" class="tabcontent tabdesign">
    <label for="user-css">User CSS</label>
    <textarea
      name="user-css"
      id="user-css"
      class="form-control fform text-input"
      style="width: 100%"
      placeholder={placeholderUserCss.replaceAll('LT', '<').replaceAll('GT', '>')}
      >{data.user_css}</textarea
    >
    <br />
    <label for="profile-css">Profile CSS</label>
    <textarea
      name="profile-css"
      id="profile-css"
      class="form-control fform text-input"
      style="width: 100%"
      placeholder="Enter any profile CSS you want here. For security purposes, this does not allow Javascript whatsoever!"
      >{data.profile_css}</textarea
    >
  </section>
</Tab>
<Button
  href={'#'}
  onclick={updateProfile}
  class="button"
  id="update-profile-btn"
  touch
  >Update Profile</Button
>
<pre>{popUpMsg}</pre>

<style>
  .connection-container {
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    background-color: rgba(255, 255, 255, 0.1);
  }

  .tabdesign {
    overflow: visible !important;
  }

  .user-username,
  .user-avatar {
    display: flex;
    opacity: 1 !important;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
  }

  .opaque {
    opacity: 0.8 !important;
  }

  .user-username {
    margin-bottom: 0px;
    padding-bottom: 0px;
  }

  .user-avatar {
    border-radius: 50%;
    width: 120px;
  }

  #user-description {
    text-align: center;
    margin: 0px;
    padding: 0px;
  }

  :global(#profiles-center) {
    margin-left: auto;
    margin-right: auto;
    display: flex !important;
    align-items: center;
    width: 150px;
    padding: 3px;
  }

  :global(.button) {
    opacity: 1 !important;
    border: solid thin !important;
  }
</style>
