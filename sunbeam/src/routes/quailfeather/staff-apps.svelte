<script context="module">
  /** @type {import('@sveltejs/kit').ErrorLoad} */
  import { apiUrl, lynxUrl } from '$lib/config';
  export const prerender = false;
  export async function load({ session }) {
    let id = '0';
    if (session.session.token) {
      id = session.session.user.id;
    } else {
      return {
        status: 401,
        error: new Error('You need to login to view this page')
      };
    }
    let perms = await fetch(`${apiUrl}/baypaw/perms/${id}`);

    perms = await perms.json();

    let staffApps = await fetch(`${lynxUrl}/staff-apps?user_id=${id}`, {
      headers: {
        Authorization: session.session.token,
        'Content-Type': 'application/json'
      }
    });

    let json = await staffApps.json();

    if (!staffApps.ok) {
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    let questions = await fetch(`${lynxUrl}/staff-apps/questions`);

    if (!questions.ok) {
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    questions = await questions.json();

    return {
      props: {
        perms: perms,
        apps: json,
        questions: questions
      }
    };
  }
</script>

<script lang="ts">
  import QuailTree from './_helpers/QuailTree.svelte';
  import Section from '$lib/base/Section.svelte';
  import Button from '$lib/base/Button.svelte';
  import { enums } from '$lib/enums/enums';
  import * as logger from '$lib/logger';
  import { session } from '$app/stores';

  export let perms;
  export let apps;
  export let questions;
</script>

<QuailTree perms={perms.perm}>
  <Section id="sapps" title="Staff Apps" icon="fluent:thinking-24-regular">
    <div class="hr-sep">
      {#if perms.perm < 2}
        <p>
          The below list of staff applications only shows applications that you have made that are
          pending review
        </p>
      {:else}
        <p>The below list of staff applications shows all applications that are pending review</p>
      {/if}
      {#each apps as app}
        <img
          loading="lazy"
          src={app.user.avatar}
          alt="{app.user.username}'s avatar"
          on:error={function () {
            this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
          }}
        />
        <p>{app.user.username}#{app.user.disc.padStart(4, 0)}</p>

        {#each app.questions as pane}
          <h3>{pane.title}</h3>
          <p>{pane.description}</p>
          {#each pane.questions as question}
            <h4>{question.title}</h4>
            <p>{question.question}</p>
            <p>Length: {question.min_length} to {question.max_length} characters</p>
            <div class="scroll-claw">
              <p>
                Answer: <span style="opacity:0.7!important;word-wrap:break-word!important"
                  >{app.answers[question.id]}</span
                >
              </p>
            </div>
            <hr />
          {/each}
        {/each}
      {/each}
      {#if apps.length === 0}
        <p>You have no staff applications pending review</p>
      {/if}
    </div>
  </Section>
  <Section id="sapps-apply" title="Apply" icon="fa-solid:certificate">
    <div class="mx-2">
      {#if questions.can_apply}
        <h1>Think you got what it takes?</h1>
        <Button
          href={'javascript:void(0)'}
          class="mx-2 button"
          
          onclick={() => {
            let inputs = [];

            questions.questions.forEach((pane) => {
              inputs.push({
                type: enums.AlertInputType.Pre,
                description: `<h3 style="color:black!important">${pane.title}</h3>${pane.description}`,
                id: pane.title
              });

              pane.questions.forEach((question) => {
                let type = enums.AlertInputType.Text;

                if (question.type == 'number') {
                  type = enums.AlertInputType.Number;
                }

                inputs.push({
                  type: type,
                  id: question.id,
                  label: question.title,
                  description: question.question,
                  placeholder: question.description,
                  minlength: question.min_length,
                  maxlength: question.max_length,
                  required: true,
                  validate: (value) => {
                    value = value.toString();
                    logger.info('StaffApp', value, 'is being validated');
                    if (question.min_length > value.length) {
                      return `${question.title} must be at least ${question.min_length} characters long`;
                    }
                    if (question.max_length < value.length) {
                      return `${question.title} must be at most ${question.max_length} characters long`;
                    }
                  }
                });
              });
            });

            alert({
              title: 'Apply',
              id: 'apply',
              message: "Lets see what you've got!",
              type: enums.AlertType.Prompt,
              inputs: inputs,
              submit: async (value) => {
                let json = { reason: '' };
                value.indexMap.forEach((index, key) => {
                  json[key] = value.toLines(index);
                });

                let res = await fetch(`${lynxUrl}/staff-apps?user_id=${$session.session.user.id}`, {
                  method: 'POST',
                  headers: {
                    Authorization: $session.session.token,
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                    answers: json
                  })
                });

                json = await res.json();

                if (!res.ok) {
                  alert({
                    id: 'apply-error',
                    title: 'Error',
                    message: json.reason,
                    type: enums.AlertType.Error
                  });
                } else {
                  alert({
                    id: 'apply-success',
                    title: 'Success',
                    message: 'Your application has been submitted',
                    type: enums.AlertType.Success
                  });
                }
              }
            });
          }}>Apply Now!</Button
        >
      {:else}
        <h1>Staff applications are closed right now...</h1>
        <h2>But to help you prepare, here are our current questions</h2>
        <div class="hr-sep">
          {#each questions.questions as pane}
            <h3>{pane.title}</h3>
            <p>{pane.description}</p>
            {#each pane.questions as question}
              <h4>{question.title}</h4>
              <p>{question.question}</p>
              <p>Length: {question.min_length} to {question.max_length} characters</p>
              <p>Is long answer?: {question.paragraph}</p>
              <p>Input type: {question.type}</p>
              <hr />
            {/each}
          {/each}
        </div>
      {/if}
    </div>
  </Section>
</QuailTree>

<style>
  .hr-sep {
    width: 90% !important;
    margin-left: auto;
    margin-right: auto;
  }

  .scroll-claw {
    max-height: 500px;
    overflow-y: scroll;
  }
</style>
