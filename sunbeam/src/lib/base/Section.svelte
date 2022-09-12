<script lang="ts">
  import Icon from '@iconify/svelte';
  import * as logger from '$lib/logger';
  export let icon: string;
  export let title: string;
  export let id: string;

  function fade(element) {
    var op = 1; // initial opacity
    var timer = setInterval(function () {
      if (op <= 0.1) {
        clearInterval(timer);
        element.style.display = 'none';
      }
      element.style.opacity = op;
      element.style.filter = 'alpha(opacity=' + op * 100 + ')';
      op -= op * 0.1;
    }, 10);
  }

  function unfade(element) {
    var op = 0.1; // initial opacity
    element.style.display = 'block';
    var timer = setInterval(function () {
      if (op >= 1) {
        clearInterval(timer);
      }
      element.style.opacity = op;
      element.style.filter = 'alpha(opacity=' + op * 100 + ')';
      op += op * 0.1;
    }, 10);
  }

  function showHideSection() {
    logger.info('Section', 'Changing section state');
    let sid = `#section-${id}`;
    let group = document.querySelector(sid) as HTMLElement;
    if (group.style.display != 'none') {
      fade(group);
    } else {
      unfade(group);
    }
  }
</script>

<div class="bot-section">
  <Icon class="white bot-section-frag" icon={icon} inline={true} height="3em" />
  <h2 class="bot-section-frag" on:click={showHideSection}>{title}</h2>
  <hr />
</div>
<div id="section-{id}">
  <slot />
</div>

<style lang="scss">
  h2 {
    font-size: 40px;
    margin: 0px;
  }

  .bot-section-frag {
    margin-right: 10px !important;
    margin-left: 10px !important;
    display: inline-block;
    cursor: pointer;
  }

  .bot-section {
    margin-left: 10px;
    margin-right: 10px;
  }
</style>
