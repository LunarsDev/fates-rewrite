<script lang="ts">
  import MultiSelect from 'svelte-multiselect';
  import type { Option } from 'svelte-multiselect';
  import RedStar from './RedStar.svelte';

  export let selected: any;
  export let options: Option[];
  export let title: string;
  export let id: string;
</script>

<label for="tags">{title} <RedStar /></label>
<div class="black">
  <MultiSelect
    options={options}
    id={id}
    bind:selected
    --sms-li-active-bg="#4f4242"
    --sms-options-bg="black"
    --sms-selected-bg="#423838"
  />
</div>

<style>
  .black {
    background-color: black !important;
  }
</style>
