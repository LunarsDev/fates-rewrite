<script lang="ts">
  import Icon from '@iconify/svelte';
  export let partner: any;
  export let icons: any;

  if (!String.prototype.replaceAll) {
    String.prototype.replaceAll = function (str, newStr) {
      // If a regex pattern
      if (Object.prototype.toString.call(str).toLowerCase() === '[object regexp]') {
        return this.replace(str, newStr);
      }

      // If a string
      return this.replace(new RegExp(str, 'g'), newStr);
    };
  }

  // https://stackoverflow.com/a/46959528
  function title(str: string) {
    return str.replaceAll('_', ' ').replace(/(^|\s)\S/g, function (t) {
      return t.toUpperCase();
    });
  }

  let links: Map<string, string> = partner.links;
</script>

<div class="partner-shell" id={partner.id}>
  <a href={partner.links.website}>
    <div class="partner">
      <img
        class="partner-img"
        src={partner.image}
        alt="{partner.name} image"
        width="100px"
        height="100px"
        on:error={function () {
          this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
        }}
      />
      <div class="partner-content">
        <h2 style="opacity: 1 !important">{partner.name}</h2>
        <p style="opacity: 1 !important">{partner.description}</p>
        {#each Object.entries(links) as link}
          <a href={link[1]} style="margin-right: 3px;">
            <Icon icon={icons[link[0]]} />
            {title(link[0])}
          </a>
        {/each}
      </div>
    </div>
  </a>
</div>
<span class="divider" />

<style lang="scss">
  $card-scale: 1.025;

  .partner {
    border-radius: 4px 4px 4px 4px;
    background-color: #111112;
    width: 90%;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 40px;
    padding: 3px;
  }

  .partner {
    -moz-box-shadow: 0px 0px 20px 5px #000;
    -webkit-box-shadow: 0px 0px 20px 5px #000;
    box-shadow: 0px 0px 20px 5px #000;
  }

  .partner:hover {
    transform: scale($card-scale, $card-scale) perspective(1px) translateZ(0);
  }

  .partner-img {
    opacity: 1 !important;
    border-radius: 50%;
    background-color: black;
    max-width: 100px;
    max-height: 100px;
    display: inline-block;
    vertical-align: top;
  }

  .partner-content {
    display: inline-block;
  }
</style>
