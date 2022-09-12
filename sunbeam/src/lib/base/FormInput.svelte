<script lang="ts">
  import { browser } from '$app/env';
  import inputstore from '$lib/inputstore';
  import RedStar from '$lib/base/RedStar.svelte';
  export let required = false;
  export let id: string;
  export let name: string;
  export let type = 'text';
  export let formclass = 'form-inp';
  export let placeholder: string;
  export let data: any = '';
  export let textarea = false;
  export let shouldUpdateInputStore = true;
  export let onchange: any = () => {};
  export let oninput: any = () => {};
  export let onkeyup: any = () => {};
  if (!data) {
    data = '';
  }

  if (shouldUpdateInputStore) {
    $inputstore.push({ id: id, required: required });
  }
</script>

<div class={formclass}>
  <label for={id}
    >{name}{#if required}<RedStar />{/if}</label
  ><br />
  {#if !textarea}
    <input
      name={id}
      id={id}
      value={data || ''}
      class="fform"
      placeholder={placeholder}
      aria-placeholder={placeholder}
      type={type}
      aria-required={required}
      required={required}
      on:change={onchange}
      on:input={oninput}
      on:keyup={onkeyup}
    /><br />
  {:else}
    <textarea
      name={id}
      id={id}
      class="fform"
      placeholder={placeholder}
      aria-placeholder={placeholder}
      type={type}
      aria-required={required}
      required={required}
      on:change={onchange}
      on:input={oninput}
      on:keyup={onkeyup}>{data || ''}</textarea
    ><br />
  {/if}
</div>
