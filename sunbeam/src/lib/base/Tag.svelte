<script lang="ts">
  import Icon from '@iconify/svelte';
  import Button from '$lib/base/Button.svelte';
  import { goto } from '$app/navigation';
  import { enums, TargetType } from '$lib/enums/enums';
  export let tags;
  export let modWidth = true; // Whether to set width to 90% or not, needed in bot pages to make showing tags look decent
  export let type: TargetType;
  export let buttonTag = false; // Button tag or not

  export let redirectUser = false;

  export let onclick = (s: string[]) => {
    // do nothing.
  };

  interface TagAction {
    func: () => void;
    text: string;
  }

  export let tagAction: TagAction = null;

  if (!tags) {
    tags = [];
  }

  export let initialSelected: string[] = [];

  // Add first maxTags to initial render view
  let selected = [];

  console.log(initialSelected);

  if (initialSelected.length > 0) {
    selected = initialSelected;
  }

  let maxTags = 4;
  let classList = 'tag-container';
  let tagClasses = 'tag-item button';
  let spanClasses = 'tag-span';

  // Don't show tags if there are less than 5
  let showButton = true;
  if (tags.length - maxTags <= 0) {
    showButton = false;
  }

  if (buttonTag) {
    modWidth = false;
    classList = 'button-tag-container';
    tagClasses = 'button-tag-item button';
    spanClasses = 'button-tag-span';
  }

  if (modWidth) {
    classList += ' width-90';
  }

  let tagsToDisplay = tags.slice(0, maxTags);

  let showingAllTags = false;

  function showAllTags() {
    if (showingAllTags) {
      showingAllTags = false;
      tagsToDisplay = tags.slice(0, maxTags);
    } else {
      showingAllTags = true;
      tagsToDisplay = tags;
    }
  }

  function selectTag(tag) {
    if (buttonTag) {
      window.location.href = tag.href;
      return;
    }

    if (redirectUser) {
      if (type == enums.TargetType.Bot) {
        goto(`/?bt=${tag.id}`);
      } else {
        goto(`/?st=${tag.id}`);
      }
      return;
    }

    tag = tag.id;

    if (selected.includes(tag)) {
      selected = selected.filter((t) => t !== tag);
    } else {
      selected.push(tag);
    }

    selected = selected;
    onclick(selected);
  }
</script>

<div class={classList}>
  {#each tagsToDisplay as tag}
    <span class={spanClasses}>
      <Button
        onclick={() => selectTag(tag)}
        id="tags-{tag.id}"
        class={tagClasses}
        href={tag.href || 'javascript:void(0)'}
      >
        {#if !buttonTag}
          <Icon class="white tag-icon" icon={tag.iconify_data} inline={false} aria-hidden="true" />
        {/if}
        {#if buttonTag}
          {tag.name}
        {:else}
          <strong>{tag.name}</strong>
        {/if}

        {#if selected.includes(tag.id)}
          <Icon class="white tag-icon" icon="mdi:check" inline={false} aria-hidden="true" />
        {/if}
      </Button>
    </span>
  {/each}
  {#if showButton}
    {#if !showingAllTags}
      <Button id="show-all-tags" class="show-all" onclick={showAllTags}
        >+{tags.length - maxTags}</Button
      >
    {:else}
      <Button id="hide-all-tags" class="show-all" onclick={showAllTags}>hide</Button>
    {/if}
  {/if}
  {#if tagAction && selected.length > 0}
    <Button class="tag-actions" onclick={tagAction.func}>{tagAction.text}</Button>
  {/if}
</div>

<span class="tag-span" />

<style lang="scss">
  :global(.button-tag-container) {
    display: inline;
  }

  :global(.tag-icon) {
    font-size: 15px;
    margin-right: 5px;
  }

  .tag-span {
    font-size: 13px;
  }

  .width-90 {
    width: 90%;
  }

  :global(.tag-item) {
    opacity: 1 !important;
    color: white !important;
    border: solid thin !important;
    outline: none !important;
    word-wrap: break-word;
    text-overflow: ellipsis;
    margin-left: 3px;
    margin-bottom: 3px;
    cursor: pointer;
    min-width: 180px !important;
  }

  .tag-container {
    margin-left: auto;
    margin-right: auto;
    line-height: 13px;
    margin-top: 5px;
  }

  :global(.show-all) {
    border: none !important;
    background-color: white !important;
    color: black !important;
    --clickcolor: #d2edf3 !important;
  }

  :global(.tag-actions) {
    border: none !important;
    background-color: rgb(193, 125, 125) !important;
    color: black !important;
    --clickcolor: #d2edf3 !important;
  }

  :global(.button-tag-item) {
    background-color: black !important;
    margin-right: 10px;
    color: white !important;
    opacity: 1 !important;
    word-wrap: break-word !important;
    font-size: 15px !important;
    border: solid 0.1px !important;
  }
</style>
