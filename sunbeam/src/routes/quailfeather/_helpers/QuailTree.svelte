<script lang="ts">
  import { lynxUrl, electroUrl } from '$lib/config';
  import { doctreeCache } from './quailcache';
  import * as logger from '$lib/logger';

  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte'; // For later
  import { session } from '$app/stores';
  import { enums } from '$lib/enums/enums';
  import { logoutUser } from '$lib/request';

  export let perms: number = 0;

  let ignore = ['index.md']; // Index may be counter-intuitive, but we add this later

  let treeDepthOne = [];
  let treeDepthTwo = {};

  // https://stackoverflow.com/a/46959528
  function title(str) {
    return str
      .replaceAll('-', ' ')
      .replaceAll('_', ' ')
      .replace(/(^|\s)\S/g, function (t) {
        return t.toUpperCase();
      });
  }

  let treeLoading = true;

  onMount(async () => {
    if ($doctreeCache && $doctreeCache.treeDepthOne && $doctreeCache.treeDepthOne.length > 0) {
      treeDepthOne = $doctreeCache.treeDepthOne;
      treeDepthTwo = $doctreeCache.treeDepthTwo;
      treeLoading = false;
      return;
    }

    logger.info('QuailTree', 'Fetching doctree');
    let doctreeRes = await fetch(`${electroUrl}/doctree`);
    let doctree = await doctreeRes.json();

    doctree.forEach((treeEl) => {
      if (ignore.includes(treeEl[0])) {
        logger.info('Shadowsight', 'Ignoring unwanted tree element', treeEl[0]);
        return;
      }

      if (treeEl.length == 1) {
        treeDepthOne.push(treeEl[0].replace('.md', ''));
      } else if (treeEl.length == 2) {
        if (treeDepthTwo[treeEl[0]] === undefined) {
          treeDepthTwo[treeEl[0]] = [];
        }
        treeDepthTwo[treeEl[0]].push(treeEl[1].replace('.md', ''));
      } else {
        logger.error('Shadowsight', `Max nesting of 2 reached`);
      }
    });

    // Sort depth two alphabetically
    treeDepthTwo = Object.keys(treeDepthTwo)
      .sort()
      .reduce((obj, key) => {
        obj[key] = treeDepthTwo[key];
        return obj;
      }, {});

    // Sort values within depth one and two alphabetically
    for (let key in treeDepthTwo) {
      treeDepthTwo[key] = treeDepthTwo[key].sort();
    }

    treeDepthOne.sort(function (a, b) {
      if (a > b) return 1;
      else return -1;
    });

    // Readd index.md
    treeDepthOne.unshift('index');

    logger.info('Shadowsight', `Parsed doctree:`, { treeDepthOne, treeDepthTwo });

    // Force some re-renders
    treeDepthOne = treeDepthOne;
    treeDepthTwo = treeDepthTwo;

    $doctreeCache = {
      treeDepthOne: treeDepthOne,
      treeDepthTwo: treeDepthTwo
    };

    treeLoading = false;
  });

  let treeShow = false;

  // Needed to cast to HTMLInputElement for ts
  function castEventToInputEl(el: any): HTMLInputElement {
    return el;
  }

  function castAnyToAnyArray(el: any): any[] {
    return el;
  }
</script>

<a
  class="ham"
  href={'javascript:void(0)'}
  on:click={() => {
    if (treeShow) treeShow = false;
    else treeShow = true;

    // Be sure to reset treeDepths
    treeDepthOne = $doctreeCache.treeDepthOne;
    treeDepthTwo = $doctreeCache.treeDepthTwo;
  }}
  aria-label="Open Menu"
>
  <Icon icon="charm:menu-hamburger" width="30px" />
  <!--Counter-intuitive but eh-->
  <span style="vertical-align: top">Show Menu</span>
</a>

<div class="grid gap-1 grid-cols-4">
  {#if treeShow}
    <style>
      .docs-quail {
        margin-left: 0px !important;
      }
    </style>
    <div class="doctree col-span-1">
      <li class="td-1 search-flex">
        <input
          id="searchbar"
          placeholder="Search"
          on:input={(e) => {
            // Check if string is empty, if so, use $doctreeCache
            let val = castEventToInputEl(e.target).value.toLowerCase().replaceAll(' ', '-');
            logger.info('SearchDocTree', val);

            if (!val) {
              treeDepthOne = $doctreeCache.treeDepthOne;
              treeDepthTwo = $doctreeCache.treeDepthTwo;
            } else {
              let newTree = [];
              $doctreeCache.treeDepthOne.forEach((el) => {
                if (el.toLowerCase().replaceAll('_', '-').replaceAll(' ', '-').includes(val)) {
                  newTree.push(el);
                }
              });
              treeDepthOne = newTree;

              // Check depth 2
              let newTreeTwo = {};
              for (let key in $doctreeCache.treeDepthTwo) {
                if (key.toLowerCase().replaceAll('_', '-').replaceAll(' ', '-').includes(val)) {
                  newTreeTwo[key] = $doctreeCache.treeDepthTwo[key];
                }
                let newArr = [];
                $doctreeCache.treeDepthTwo[key].forEach((el) => {
                  if (el.toLowerCase().replaceAll('_', '-').replaceAll(' ', '-').includes(val)) {
                    newArr.push(el);
                  }
                });
                if (newArr.length > 0) {
                  newTreeTwo[key] = newArr;
                }
              }

              treeDepthTwo = newTreeTwo;
            }
          }}
        />
      </li>
      {#if treeLoading}
        <span class="span">Loading doctree</span>
      {/if}
      <!--Tree depth one -->
      <li class="td-1">
        <a class="tree-link" id="docs-_root-nav" href="/quailfeather">
          <span class="span">Back to root</span>
        </a>
      </li>

      <li class="td-1">
        <a class="tree-link" id="requests-nav" href="/quailfeather/requests">
          <span class="span">Public Admin Request Logs</span>
        </a>
      </li>

      {#if perms > 2}
        <li class="td-1">
          <a
            class="tree-link"
            id="staff-verify-nav"
            href={'javascript:void(0)'}
            on:click={() => {
              alert({
                id: 'staff-verify-alert',
                title: 'Staff Verification',
                type: enums.AlertType.Prompt,
                message: `
<h3 style="color:black!important">In order to continue, you will need to make sure you are up to date with our rules</h3>
<strong>You can find our staff guide <a style="color:blue!important" href="/quailfeather/docs/staff-guide">here</a></strong>
<ol style="color:black!important">
	<li>The code is somewhere in the staff guide so please read the full guide</li>
	<li>Look up terms you do not understand on Google!</li>
</ol>
<strong style="color:black!important">Once you complete this, you will automatically recieve your roles in the staff server</strong>
<strong>By continuing, you agree to:</strong>
<ol style="color:black!important">
	<li>Abide by Discord ToS</li>
	<li>Abide by Fates List ToS</li>
	<li>Agree to try and be at least partially active on the list</li>
	<li>Be able to join group chats (group DMs) if required by Fates List Admin+</li>
</ol>
If you disagree with any of the above, you should stop now and consider taking a 
Leave Of Absence or leaving the staff team though we hope it won't come to this...<br/><br/>

Please <em>read</em> the staff guide carefully. Do NOT just Ctrl-F. If you ask questions already
in the staff guide, you will just be told to reread the staff guide!`.replaceAll('\n', ''),
                input: {
                  id: 'Code',
                  label: 'Code',
                  required: true,
                  multiline: false,
                  placeholder: 'Enter code here',
                  type: enums.AlertInputType.Text
                },
                submit: async (value) => {
                  let code = value.toString();
                  logger.info(code, 'Code');
                  let res = await fetch(
                    `${electroUrl}/ap/newcat?user_id=${$session.session.user.id}`,
                    {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                        Authorization: $session.session.token
                      },
                      body: code
                    }
                  );

                  if (res.ok) {
                    let data = await res.json();
                    alert(
                      `Staff verified! Your lynx password is:
											
<code style="word-wrap:break-word!important;overflow-y:scroll!important;">${data.pass}</code>

Please enter <code>${data.totp_shared_key}</code> in Google Authenticator or Authy for 2FA verification.

<img src="${data.image}" alt="QR code totp"/>
`
                    );
                    return;
                  } else {
                    let data = await res.text();
                    alert(data);
                    return;
                  }
                },
                close: () => {}
              });
            }}
          >
            <span class="span">Staff Verify</span>
          </a>
        </li>
        <li class="td-1">
          <a class="tree-link" id="loa-nav" href="/quailfeather/loa">
            <span class="span">File Leave Of Absence</span>
          </a>
        </li>
        <li class="td-1">
          <a class="tree-link" id="sapp-nav" href="/quailfeather/staff-apps">
            <span class="span">Staff Applications</span>
          </a>
        </li>
        <li class="td-1">
          <a class="tree-link" id="admin-nav" href="/quailfeather/admin">
            <span class="span">Admin Panel</span>
          </a>
        </li>
        <li class="td-1">
          <a
            class="tree-link"
            id="reset-nav"
            href={'javascript:void(0)'}
            on:click={() => {
              alert({
                title: 'Reset',
                message: 'Enter 2FA code here',
                type: enums.AlertType.Prompt,
                submit: async (v) => {
                  let res = await fetch(`${lynxUrl}/reset?user_id=${$session.session.user.id}`, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                      Authorization: $session.session.token,
                      'Frostpaw-MFA': v.toRaw()
                    }
                  });

                  if (res.ok) {
                    alert({
                      id: 'reset-alert',
                      title: 'Success',
                      type: enums.AlertType.Success,
                      close: () => {
                        logoutUser();
                      },
                      message: `Successfully reset credentials. You will need to login again.`
                    });
                  }
                },
                inputs: [
                  {
                    id: 'mfa-key',
                    label: '2FA Code',
                    placeholder: '2FA Code',
                    required: true,
                    type: enums.AlertInputType.Number
                  }
                ]
              });
            }}
          >
            <span class="span">Reset Credentials</span>
          </a>
        </li>
      {/if}

      {#each treeDepthOne as el}
        <li class="td-1">
          <a class="tree-link" id="docs-{el}-nav" href="/quailfeather/docs/{el}">
            <span class="span">{title(el.replace('-', ' '))}</span>
          </a>
        </li>
      {/each}

      <!--Depth two-->
      {#each Object.entries(treeDepthTwo) as [tree, childs]}
        <li id="docs-{tree}-nav" class="td-1">
          <details>
            <summary class="span">{title(tree.replace('-', ' '))}</summary>
            <ul>
              {#each castAnyToAnyArray(childs) as child}
                <li>
                  <a
                    class="tree-link"
                    id="docs-{tree}-{child}-nav"
                    href="/quailfeather/docs/{tree}/{child}"
                  >
                    <span class="span">{title(child.replace('-', ' '))}</span>
                  </a>
                </li>
              {/each}
            </ul>
          </details>
        </li>
      {/each}
    </div>
  {:else}
    <style>
      .content {
        width: 100%;
        display: block;
      }

      .col-span-3 {
        grid-column: span 4 / span 3;
      }
    </style>
  {/if}
  <!--Never ever rerender this, it can be very very expensive-->
  <div class="content col-span-3">
    <slot />
  </div>
</div>

<style lang="scss">
  .doctree {
    min-height: 1vh;
  }

  .doctree {
    z-index: 2;
    position: sticky !important;
    top: 0;
    left: 0;
    background: lightgrey;
    color: black !important;
  }

  .span {
    color: black !important;
    opacity: 1 !important;
    font-size: 18px;
  }

  .td-1 {
    list-style: none !important;
    padding: 5px !important;
    border-bottom: 1px solid black !important;
  }

  @media only screen and (max-width: 600px) {
    .span {
      font-size: 12px !important;
    }
  }

  .tree-link {
    opacity: 1 !important;
  }

  .search-flex {
    display: flex;
    flex-wrap: wrap;
  }

  #searchbar {
    background: #444;
    padding: 0 20px;
    border: none;
    border-radius: 4px;
    color: #ffffff;
    height: 30px;
    margin: 0 !important;
    width: 100% !important;
    overflow-x: hidden !important;
  }

  .ham {
    font-size: 18px;
    padding: 3px;
  }
</style>
