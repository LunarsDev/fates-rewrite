<script lang="ts">
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  let serverBotInvite = 'https://fateslist.xyz/bot/811073947382579200/invite';
</script>

<BristlefrostMeta
  title="Add your servers on Fates List!"
  description="Fates List server listing is a great way to get active members for your server"
  thumbnail="https://fateslist.xyz/static/botlisticon.webp"
  url="https://fateslist.xyz/frostpaw/add-server"
/>
<h1>Add Server</h1>
<h2>
  To add your server, add <a href={serverBotInvite}>our bot</a> to your server then run /set.
</h2>
<h3>Next steps</h3>
<ul>
  <li>Set a description (and a long description) otherwise it will be randomly generated!</li>
  <li>See our full set of ever-growing features using /help!</li>
</ul>

<style lang="scss">
  ul {
    color: white;
  }
</style>
