<script lang="ts">
  import { loginUser, request } from '$lib/request';
  import { page } from '$app/stores';
  import { browser } from '$app/environment';
    import { api } from '$lib/config';
    import Button from '$lib/base/Button.svelte';

  export let data: {all_permissions: any, action: string};

   if (!$page.data.token) {
    if (browser) {
      loginUser({
        allowBanned: true
      });
    }
  }

  async function makeReq() {
    let userId = null
    if($page.data.permissions.index < data.all_permissions["sudo"].index) {
      userId = $page.data.user.id;
    } else {
      userId = (document.querySelector("#user_id") as HTMLInputElement).value
    }

    let act = (document.querySelector("#action") as HTMLSelectElement).value

    let resp = await request(`${api}/data?user_id=${userId}&mode=${act}`, {
      method: 'GET',
      session: $page.data,
      fetch: fetch,
      endpointType: "user",
      auth: true
    });
    
    if(!resp.ok) {
      alert("Error: " + JSON.stringify(await resp.json()))
    } else {
      let json = await resp.json();

      alert(json.task_id)
    }
  }
</script>

{#if $page.data.token}

  {#if $page.data.permissions.index < data.all_permissions["sudo"].index}
    <p>You are only allowed to perform a data action on your *own* user ID</p>
  {:else}
    <div style="width: 80%">
      <label for="user_id">User ID</label>
      <input class="fform" id="user_id" name="user_id" type="text" value={$page.data.user.id} />
    </div>
  {/if}

  <select name="action" id="action">
    {#if data.action == "req"}
      <option value="req" selected>Request</option>
    {:else}
      <option value="req">Request</option>
    {/if}
    {#if data.action == "del"}
      <option value="del" selected>Delete</option>
    {:else}
      <option value="del">Delete</option>
    {/if}
  </select>

  <Button onclick={() => makeReq()}>Next</Button>
{:else}
  <p>Logging you in, please wait...</p>
{/if}
