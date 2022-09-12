<div class="card-container">
  <slot />
</div>

<style>
  .card-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    padding-left: 0;
  }

  slot {
    list-style: none;
    flex: 0 0 33%;
    justify-content: center;
    align-items: center;
  }
</style>
