<script lang="ts">
  import { onMount } from 'svelte';

  import * as logger from '$lib/logger';

  import quillstore from '$lib/quillstore';

  export let placeHolderContent: string;
  export let id: string;
  export let value: string;

  let options = {
    placeholder: placeHolderContent
  };

  let editor;

  onMount(async () => {
    // Packages
    const quillImport = await import('quill');

    logger.info('Quill', 'Have imported quill');

    const Quill = quillImport.default;
    Quill.imports = quillImport.imports;

    // Editor
    const quill = new Quill(editor, {
      modules: {
        theme: undefined,
        toolbar: false
      },
      placeholder: options.placeholder
    });

    if (value) {
      quill.setText(value, 'silent');
    }

    if (!$quillstore) {
      $quillstore = new Map();
    }

    $quillstore.set(id, quill);
    $quillstore = $quillstore;

    // Quill (Editor) Markdown Extension
    const markdownOptions = {};

    if (window.QuillMarkdown) {
      logger.info('Loading quill-markdown');
      let _ = new window.QuillMarkdown(quill, markdownOptions);
    }
  });
</script>

<div bind:this={editor} id={id} tabindex="0" style="overflow-x: hidden;" />

<style>
  @import '../../css/texteditor.css';
</style>
