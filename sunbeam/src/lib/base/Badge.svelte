<script lang="ts">
  export let badge;

  import { goto } from '$app/navigation';
  import { enums } from '$lib/enums/enums';
  let isHovering = false;
</script>

<div id={badge.id} class="badge-item">
  <div class="badge-hover" class:selected={isHovering} id={badge.id} aria-live="polite">
    <span class="badge-hover-text">{badge.name}</span>
  </div>

  <div
    class="badge-link"
    on:click={() => {
      if (badge.link) {
        goto(badge.link);
        return;
      }

      alert({
        title: badge.name,
        message: badge.description,
        id: badge.id,
        icon: badge.icon,
        type: enums.AlertType.Info
      });
    }}
    on:mouseleave={() => (isHovering = false)}
  >
    <img
      id="badge-icon-{badge.id}"
      class="badge-img"
      src={badge.icon}
      width="50px"
      height="50px"
      alt={badge.description}
      on:error={function () {
        this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
      }}
    />
  </div>
</div>

<style>
  .badge-item {
    max-width: 50px !important;
  }

  .selected {
    visibility: visible !important;
  }

  .badge-hover-text {
    overflow: visible !important;
    white-space: nowrap !important;
    text-align: center !important;
  }

  .badge-hover {
    text-align: center !important;
    overflow: visible;
    align-items: center;
    justify-content: center;
    background-color: black;
    color: white;
    visibility: hidden;
    display: inline;
  }

  .badge-link {
    cursor: pointer;
  }

  .badge-img {
    border-radius: 50%;
    margin-right: 15px;
  }

  .badge-item {
    align-items: center;
    justify-content: center;
  }
</style>
