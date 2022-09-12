<script lang="ts">
  export let data: boolean;
  export let id: string;
</script>

{#if !data}
  <input type="checkbox" id={id} name={id} />
{:else}
  <input type="checkbox" id={id} name={id} checked />
{/if}
<label for={id}><slot /></label>
<br />
