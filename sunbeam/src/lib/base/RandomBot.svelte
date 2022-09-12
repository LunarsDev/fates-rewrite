<script lang="ts">
  import Button from '$lib/base/Button.svelte';
  import BotCard from '$lib/cards/BotCard.svelte';
  import { roll } from '$lib/request';
  export let type: string;

  export let randomBot: any;

  async function roller() {
    randomBot = await roll(type, fetch);
  }
</script>

<div class="flex">
  <BotCard type={type} rand={false} data={randomBot} />
  <Button
    id="random-bot"
    class="random-button white button"
    onclick={() => {
      roller();
    }}>Roll</Button
  >
</div>
<div class="spacer" />

<style>
  .spacer {
    margin-bottom: 10px;
  }
  .flex {
    margin-left: auto;
    margin-right: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }
  :global(.random-button) {
    display: flex !important;
    border: solid thin !important;
    outline: none !important;
  }
</style>
