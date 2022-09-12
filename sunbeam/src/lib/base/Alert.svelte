<script lang="ts">
  import quillstore from '$lib/quillstore';
  import * as logger from '$lib/logger';
  import { storage } from '$lib/supabase';
  import TextEditor from '$lib/base/TextEditor.svelte';
  import { session } from '$app/stores';
  import { AlertType, enums } from '$lib/enums/enums';

  export let show: boolean;
  export let icon: string;
  export let close;
  export let submit;
  export let inputs: any[];
  export let buttons: any[];
  export let showError = false;

  export let supabase;

  if ($session.session.token) {
    supabase = new storage($session.session.user.id, $session.session.token, false);
  } else {
    supabase = new storage(null, null, false);
  }

  setTimeout(() => {
    supabase.getBucket('public').then((data) => {
      logger.info('Supabase', data);
    });
  }, 5000);

  let editor; // We bind to this
  let error: string = '';
  let errTgt: string = '';

  const closeAlert = () => {
    if (close) {
      close();
    }
    show = false;
  };

  class SubmittedInput {
    inputs: any;
    defaultIndex: number; // Default index to use in toSingleLine
    indexMap: Map<String, number>; // Map of input id to index
    values: Map<number, string>; // Map of index to value (for number/boolean etc only)

    constructor(editor: object, inputs: any) {
      this.inputs = inputs;
      this.defaultIndex = 0;
      this.indexMap = this.createIndexMap();
    }

    createIndexMap() {
      let map = new Map<String, number>();
      let valueMap = new Map<number, string>();

      for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].type == enums.AlertInputType.Pre) {
          continue;
        }

        map.set(inputs[i].id, i);

        if (
          inputs[i].type == enums.AlertInputType.Number ||
          inputs[i].type == enums.AlertInputType.Boolean
        ) {
          valueMap.set(i, (document.querySelector(`#inp-${i}`) as HTMLInputElement).value);
        }
      }

      logger.info('Made valueMap of: ', valueMap);

      this.values = valueMap;
      return map;
    }

    getIndex(index: number = -1) {
      logger.info('getIndex', index);
      if (typeof index == 'string') {
        logger.info('AlertBox', 'Got indexMap of:', this.indexMap);
        return this.indexMap.get(index) || this.defaultIndex;
      }

      if (index == -1) {
        return this.defaultIndex;
      }

      return index;
    }

    toSingleLine(index: number = -1) {
      // Does exactly what it says it does on the tin, returns a single no-newline line
      index = this.getIndex(index);
      return this.toRaw(index)
        .replaceAll('\n', ' ')
        .replaceAll('\r', ' ')
        .replaceAll('\t', '')
        .trim();
    }

    toLines(index: number = -1) {
      let gotIndex = this.getIndex(index);

      let raw = this.toRaw(gotIndex);

      logger.info('AlertBox', 'Got raw:', raw);

      if (inputs[gotIndex].type == enums.AlertInputType.Number) {
        return raw;
      }

      let split = raw.replaceAll('\r', '\n').split('\n');

      let result = [];

      let gotToContent = false;

      for (let i = 0; i < split.length; i++) {
        if (this.trim(split[i]) != '') {
          gotToContent = true;
        }

        if (gotToContent) {
          result.push(split[i]);
        }
      }

      // If last line is \n then remove it
      for (let i = result.length; i >= 0; i--) {
        if (!this.trim(result[result.length - 1])) {
          result.pop();
        } else {
          break;
        }
      }

      logger.info('AlertBox', 'Got validated lines', result);

      return result.join('\n');
    }

    toDelta(index: number = -1) {
      index = this.getIndex(index);

      let obj = inputs[index];

      if (obj.type == enums.AlertInputType.Text) {
        return $quillstore.get(`inp-${index}`).getContents();
      }
      return null; // No quill textbox
    }

    trim(s: string) {
      return s.replaceAll(' ', '').replaceAll('\n', '').replaceAll('\t', '').replaceAll('\r', '');
    }

    focusError() {
      (document.querySelector(`#${errTgt}`) as HTMLElement).scrollIntoView();
    }

    validate() {
      showError = false;
      logger.info('AlertBox', `Validating ${inputs.length} inputs`);
      for (let i = 0; i < inputs.length; i++) {
        this.defaultIndex = i;

        let input = inputs[i];

        if (showError) {
          return showError;
        }

        if (input.type == enums.AlertInputType.Pre) {
          continue;
        }

        if (input.type == enums.AlertInputType.File) {
          continue;
        }

        logger.info('AlertBox', { input });

        if (input.required) {
          const checks = this.trim(this.toRaw());

          if (checks === '') {
            showError = true;
            error = 'Error: This field is required';
            errTgt = `inp-${i}`;
            this.focusError();
            return showError;
          } else {
            showError = false;
            error = '';
          }
        }

        if (input.validate) {
          let check = input.validate(this);
          if (check) {
            showError = true;
            error = check;
            errTgt = `inp-${i}`;

            this.focusError();
            return showError;
          }
        }
      }

      this.defaultIndex = 0;
      return showError;
    }

    toRaw(index: number = -1) {
      index = this.getIndex(index);

      logger.info('AlertBox', 'toRaw of index', index);

      let obj = inputs[index];

      let content;

      if (obj.type == enums.AlertInputType.Text) {
        content = $quillstore.get(`inp-${index}`).getText();
      } else {
        // This returns the raw output with \n's
        content = this.values.get(index);
      }

      return content;
    }

    toString() {
      // Prototype Object.prototype.toString (i hope this works)
      return this.toLines();
    }
  }

  export let uploadedFiles: any[] = [];

  const onFileAdded = (data) => {
    const files = data.target.files;

    files.forEach((file) => {
      const metadata = {
        name: file.name,
        size: file.size,
        extension: file.type || 'Unknown',
        last_updated: file.lastModified
      };

      uploadedFiles.push(metadata);
      uploadedFiles = uploadedFiles;
      logger.info('FileAdded', metadata);
    });
  };

  const submitInput = () => {
    logger.info('AlertBox', 'Clicked submit');
    errTgt = null;

    if (inputs && inputs.length > 0 && submit) {
      logger.info('AlertBox', 'Found input');
      const inp = new SubmittedInput(editor, inputs);
      const valid = inp.validate();

      inputs.forEach(async (input) => {
        switch (input.type) {
          case enums.AlertInputType.File:
            let element = document.getElementById(
              `inp-${inp.getIndex(input.id)}`
            ) as HTMLInputElement;

            /*const data = await supabase.uploadFiles('public', element.files).catch((err) => {
							console.error(err);
						});

						console.log(data);*/

            console.log('Files cannot be uploaded at this time');
            break;

          default:
            return;
            break;
        }
      });

      logger.info('AlertBox', `Got validator ${valid}`);

      if (valid) {
        return;
      }

      submit(inp);
    }

    closeAlert();
  };

  export let title: string;
  export let id: string;
  export let type: AlertType;
</script>

<svelte:head>
  <!--Blame svelte-->
  <script
    src="https://cdn.jsdelivr.net/npm/quilljs-markdown@latest/dist/quilljs-markdown.js"></script>
</svelte:head>

{#if show}
  <!-- svelte-ignore a11y-no-redundant-roles -->
  <dialog open role="dialog" aria-labelledby={`${id}-title`} aria-describedby={`${id}-content`}>
    <section>
      <h1 id={`${id}-type`} class="alert-type">{enums.AlertType[type] || 'Unknown'}</h1>

      <header id={`${id}-title`}>
        <strong>
          <div class="alert-header">
            {#if icon}
              <img
                class="alert-icon"
                src={icon}
                alt={`${id} icon`}
                height="25px"
                width="25px"
                on:error={function () {
                  this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
                }}
              />
            {/if}

            <h2 class="alert-title">{title}</h2>
          </div>
        </strong>
      </header>

      <div id={`${id}-content`} class="alert-content">
        <slot />

        {#if inputs && inputs.length > 0}
          <br />

          {#each inputs as inputData, id}
            {#if inputData}
              {#if inputData.type != enums.AlertInputType.Pre}
                <br />
                <fieldset>
                  <legend>{inputData.label}</legend>

                  {#if inputData.description}
                    <span>{inputData.description}</span>
                  {/if}

                  {#if inputData.type == enums.AlertInputType.Number}
                    <label for="alert-input" class="alert-label">{inputData.label}</label>

                    <input id="inp-{id}" type="number" class="InputAlert" />

                    {#if inputData.placeholder}
                      <small>{inputData.placeholder}</small>
                    {/if}

                    {#if inputData.minlength || inputData.maxlength}
                      <br />
                    {/if}
                    {#if inputData.minlength}
                      <small>Minimum Length: {inputData.minlength}</small>
                    {/if}
                    {#if inputData.maxlength}
                      {#if inputData.minlength}
                        <br />
                      {/if}
                      <small>Maximum Length: {inputData.maxlength}</small>
                    {/if}

                    {#if (!errTgt || errTgt == `inp-${id}`) && showError}
                      <div class="input-error">{error}</div>
                    {/if}
                  {/if}

                  {#if inputData.type == enums.AlertInputType.Boolean}
                    <label for="alert-input" class="alert-label">{inputData.label}</label>

                    <input
                      id="inp-{id}"
                      type="checkbox"
                      class="InputAlert"
                      placeholder={inputData.placeholder}
                    />

                    {#if (!errTgt || errTgt == `inp-${id}`) && showError}
                      <div class="input-error">{error}</div>
                    {/if}
                  {/if}

                  {#if inputData.type == enums.AlertInputType.DateTime}
                    <label for="alert-input" class="alert-label">{inputData.label}</label>

                    <input
                      id="inp-{id}"
                      type="datetime"
                      class="InputAlert"
                      placeholder={inputData.placeholder}
                    />

                    {#if (!errTgt || errTgt == `inp-${id}`) && showError}
                      <div class="input-error">{error}</div>
                    {/if}
                  {/if}

                  {#if inputData.type == enums.AlertInputType.DateTimeLocal}
                    <label for="alert-input" class="alert-label">{inputData.label}</label>

                    <input
                      type="datetime-local"
                      id="inp-{id}"
                      class="InputAlert"
                      placeholder={inputData.placeholder}
                    />

                    {#if (!errTgt || errTgt == `inp-${id}`) && showError}
                      <div class="input-error">{error}</div>
                    {/if}
                  {/if}

                  {#if inputData.type == enums.AlertInputType.Color}
                    <label for="alert-input" class="alert-label">{inputData.label}</label>

                    <input
                      id="inp-{id}"
                      type="color"
                      class="InputAlert"
                      placeholder={inputData.placeholder}
                    />

                    {#if (!errTgt || errTgt == `inp-${id}`) && showError}
                      <div class="input-error">{error}</div>
                    {/if}
                  {/if}

                  {#if inputData.type == enums.AlertInputType.File}
                    <label for="alert-input" class="alert-label">{inputData.label}</label>

                    {#if inputData.multipleFiles}
                      <input
                        id="inp-{id}"
                        type="file"
                        multiple={true}
                        class="InputAlert"
                        on:input={(data) => {
                          onFileAdded(data);
                        }}
                      />
                    {:else}
                      <input
                        id="inp-{id}"
                        type="file"
                        multiple={false}
                        class="InputAlert"
                        on:input={(data) => {
                          onFileAdded(data);
                        }}
                      />
                    {/if}

                    <button
                      on:click={() => {
                        document.getElementById(`inp-${id}`).click();
                      }}>Upload Files</button
                    >

                    <ol id="files">
                      {#each uploadedFiles as file}
                        <li class="File">
                          {#if file.error}
                            <span class="File-Error">{file.error}</span>
                          {:else}
                            <h2 class="File-Name">Name: {file.name}</h2>
                            <p class="File-Extension">Extension: {file.extension}</p>
                            <p class="File-Bytes">Bytes: {file.size}</p>
                          {/if}
                        </li>
                      {/each}
                    </ol>

                    <h2 class="InputAlert-Placeholder">{inputData.placeholder}</h2>

                    {#if (!errTgt || errTgt == `inp-${id}`) && showError}
                      <div class="input-error">{error}</div>
                    {/if}
                  {/if}

                  {#if inputData.type == enums.AlertInputType.Text}
                    <label for="alert-input" class="alert-label">{inputData.label}</label>

                    <TextEditor
                      value={inputData.value || ''}
                      id="inp-{id}"
                      placeHolderContent={inputData.placeholder}
                    />

                    {#if inputData.minlength || inputData.maxlength}
                      <br />
                    {/if}
                    {#if inputData.minlength}
                      <small>Minimum Length: {inputData.minlength}</small>
                    {/if}
                    {#if inputData.maxlength}
                      {#if inputData.minlength}
                        <br />
                      {/if}
                      <small>Maximum Length: {inputData.maxlength}</small>
                    {/if}

                    {#if (!errTgt || errTgt == `inp-${id}`) && showError}
                      <div class="input-error">{error}</div>
                    {/if}
                  {/if}
                </fieldset>
              {:else}
                {@html inputData.description}
                <br />
              {/if}
            {/if}
          {/each}

          <button type="button" on:click={submitInput}>Submit</button>
        {/if}
      </div>

      <div class="buttons">
        {#if buttons && buttons.length > 0}
          {#each buttons as buttonData}
            {#if buttonData}
              <button
                type="button"
                on:click={() => {
                  buttonData.function();
                }}>{buttonData.name}</button
              >
            {/if}
          {/each}
        {/if}
      </div>

      <button on:click={closeAlert} id="alert-close" class="block mx-auto"> Close </button>
    </section>
  </dialog>
{/if}

<style>
  /* Basic Shit */
  dialog {
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    z-index: 9999;
    height: 100%;
    overflow-x: scroll;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: transparent;
    color: black !important;
  }

  :global(.alert-content) {
    color: black !important;
  }

  slot {
    color: black !important;
  }

  dialog::after {
    content: '';
    display: block;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: black;
    opacity: 0.5;
    z-index: -1;
    pointer-events: none;
  }

  section {
    width: 500px;
    min-height: 200px;
    max-height: 100%;
    padding: 10px;
    border-radius: 4px 4px 4px 4px;
    background: rgb(31, 28, 28);
    color: white;
    overflow-y: scroll;
  }

  button {
    background-color: rgb(47, 40, 40) !important;
    color: white !important;
    font-weight: bold !important;
    border: black solid 1px !important;
    padding: 12px;
    border-radius: 5px;
    margin-top: 10px;
    cursor: pointer;
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      transform: scale(1);
    }
  }

  button:hover {
    animation: pulse 1s infinite;
    background-color: black !important;
    color: white !important;
  }

  /* Fieldset */
  fieldset {
    border-radius: 6px;
    overflow-x: scroll;
  }

  legend {
    font-family: 'Fira Code', monospace;
    font-weight: bold;
  }

  /* Alert */
  .alert-type {
    color: white !important;
    font-weight: bold;
    font-size: 15px;
  }

  .alert-title {
    color: white !important;
  }

  .alert-content {
    color: white !important;
    margin-left: 15px;
  }

  .alert-icon {
    height: 25px;
    width: 25px;
    border-radius: 50%;
    padding: 5px;
    background: black;
  }

  .alert-icon + .alert-title {
    margin-left: 10px;
  }

  .alert-header {
    display: flex;
    align-items: center;
    margin-left: 15px;
  }

  #alert-close {
    position: relative;
    text-align: center !important;
    margin-top: 45px;
    cursor: pointer;
  }

  /* Input */
  .InputAlert {
    width: 100%;
    height: 40px;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0 10px;
    font-size: 14px;
    color: #333;
    margin-top: 10px;
    overflow: hidden;
  }

  .InputAlert[type='number'] {
    width: 95%;
    background-color: black;
    color: #1e90ff;
  }

  .InputAlert[type='file'] {
    display: none;
    margin: 0;
    padding: 0;
    border: none;
  }

  .InputAlert[type='number'] {
    overflow-x: scroll !important;
  }

  .InputAlert-Placeholder {
    color: white !important;
    font-family: 'Fira Code', monospace;
    font-weight: bold;
    font-size: 16px;
    margin-top: 20px;
    margin-bottom: 0;
  }

  .input-error {
    background-color: red;
    color: white;
    font-weight: bold;
    padding: 10px;
    margin-top: 10px;
    border-radius: 7px;
  }

  .alert-label {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }

  /* File */
  #files {
    list-style: none;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 20px;
    overflow: scroll;
  }

  .File {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px;
  }

  .File::after {
    margin-bottom: 5px;
  }

  .File-Name {
    color: white !important;
    font-weight: bold;
    font-size: 15px;
  }

  .File-Extension {
    color: white !important;
    font-weight: bold;
    font-size: 10px;
  }

  .File-Bytes {
    color: white !important;
    font-weight: bold;
    font-size: 10px;
  }

  .File-Error {
    background-color: red;
    color: white;
    font-weight: bold;
    padding: 10px;
    margin-top: 10px;
    border-radius: 7px;
  }

  /* Responsive (Mobile) */
  @media screen and (max-width: 560px) {
    dialog {
      position: fixed;
      top: 0;
      right: 0;
      left: 0;
      bottom: 0;
      z-index: 9999;
      height: 100%;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      background: transparent;
      color: white !important;
    }

    dialog::after {
      content: '';
      display: block;
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      background: black;
      opacity: 0.5;
      z-index: -1;
      pointer-events: none;
    }

    section {
      width: 75%;
      min-height: 200px;
      max-height: 500px;
      padding: 10px;
      border-radius: 4px 4px 4px 4px;
      background: rgb(31, 28, 28);
      color: white !important;
    }
  }
</style>
