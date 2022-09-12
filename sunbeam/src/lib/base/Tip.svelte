<script lang="ts">
  import Icon from '@iconify/svelte';
  export let alertClass = 'alert-info tip-blue';
  export let icon = 'foundation:lightbulb';
</script>

<p class={alertClass}>
  <Icon icon={icon} inline={false} height="1.2em" style="margin-right: 1px" />
  <slot />
</p>

<style lang="scss">
  p {
    font-weight: normal !important;
  }

  :global(.tip-blue) {
    background: rgba(37, 157, 176, 0.75) !important;
  }

  :global(.alert-info) {
    padding: 10px;
    border-radius: 4px 4px 4px 4px;
  }
</style>
