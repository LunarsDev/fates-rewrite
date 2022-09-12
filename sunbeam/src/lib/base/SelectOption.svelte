<script lang="ts">
  export let value: string;
  export let masterValue: string;
  export let disabled: boolean = false;
</script>

{#if `${masterValue}` == `${value}`}
  {#if disabled}
    <option value={value} selected disabled><slot /></option>
  {:else}
    <option value={value} selected><slot /></option>
  {/if}
{:else if disabled}
  <option value={value} disabled><slot /></option>
{:else}
  <option value={value}><slot /></option>
{/if}
