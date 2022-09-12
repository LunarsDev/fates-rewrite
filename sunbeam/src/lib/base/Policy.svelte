<script lang="ts">
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
  export let policy: any;
</script>

<!--section[0] - Key, section[1] - Value-->
{#each Object.entries(policy) as section}
  <h1>{title(section[0])}</h1>
  {#if Array.isArray(section[1])}
    <ol>
      {#each section[1] as sectionData}
        <li>{sectionData}</li>
      {/each}
    </ol>
  {:else}
    {#each Object.entries(section[1]) as sectionData}
      <h2>{title(sectionData[0])}</h2>
      {#if Array.isArray(sectionData[1])}
        <ol>
          {#each sectionData[1] as policy}
            <li>{policy}</li>
          {/each}
        </ol>
      {:else}
        <p>{sectionData[1]}</p>
      {/if}
    {/each}
  {/if}
{/each}

<style>
  p {
    margin-left: 3px;
  }
</style>
