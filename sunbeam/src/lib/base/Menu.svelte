<script lang="ts">
  import menustore from '$lib/menustore';

  interface MenuElement {
    id: string;
    label: string;
    action: () => any;
  }

  export let els: MenuElement[];

  export let id: string; // Must be set in menustore to open clode
</script>

{#if $menustore.open == id}
  <div class="dropdown">
    <div id={id} class="dropdown-content">
      {#each els as el}
        <a
          href={'javascript:void(0)'}
          id={el.id}
          on:click={() => {
            let postfn = el.action();
            $menustore.open = '';
            if (postfn) {
              postfn();
            }
          }}>{el.label}</a
        >
      {/each}
    </div>
  </div>
{/if}

<style>
  .dropdown {
    position: relative;
    overflow: visible !important;
    margin-top: 0px !important;
  }

  .dropdown-content {
    overflow: visible !important;
    display: block;
    position: absolute;
    background-color: black;
    min-width: 160px;
    z-index: 1;
    margin-top: 0px !important;
    border-radius: 4px;
  }

  .dropdown-content a {
    color: white !important;
    opacity: 1 !important;
    padding: 12px 16px;
    display: block;
  }

  .dropdown a:hover {
    background-color: rgb(70, 53, 53);
  }
</style>
