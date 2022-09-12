<script lang="ts" context="module">
  import markdownit from 'markdown-it';
  import markdownItAnchor from 'markdown-it-anchor';
  import markdownitContainer from 'markdown-it-container';

  import hljs from 'highlight.js';

  export const prerender = false;
  export async function load({ params, url, fetch, session, stuff }) {
    let id = '0';
    if (session.session.token) {
      id = session.session.user.id;
    }
    let perms = await fetch(`${apiUrl}/baypaw/perms/${id}`);
    let res = await fetch(`${electroUrl}/docs/${params.route || 'index'}`);
    if (res.ok) {
      let json = await res.json();
      let data = json.data;
      let js = json.js;

      let md = markdownit({
        html: true,
        linkify: true,
        highlight: function (str, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              let v =
                `<div class="hljs-quail-block"><span class="hljs-snip">${lang}</span>` +
                hljs.highlight(str, { language: lang }).value +
                '</div>';
              return v;
            } catch (__) {}
          }

          return ''; // use external default escaping
        }
      });

      md.use(markdownItAnchor, {
        permalink: markdownItAnchor.permalink.linkInsideHeader({
          symbol: '\u00B6'
        }),
        slugify: (s) => {
          return s
            .toLowerCase()
            .replaceAll(')', '')
            .replaceAll('!', '')
            .replaceAll('.', '')
            .replace(/[^a-zA-Z0-9]/g, '-')
            .replaceAll('--', '-');
        },
        level: [1, 2, 3, 4, 5]
      });
      md.use(markdownitContainer, 'info');
      md.use(markdownitContainer, 'warning');
      md.use(markdownitContainer, 'aonly');
      md.use(markdownitContainer, 'guidelines');
      md.use(markdownitContainer, 'generic', {
        validate: function (...args) {
          return true;
        }
      });

      // Create toc
      let toc = `## Table Of Contents\n`;

      let splitDat: string[] = data.split('\n');

      try {
        for (let i = 0; i < splitDat.length; i++) {
          if (splitDat[i].startsWith('## ')) {
            toc += `- [${splitDat[i].replace('## ', '')}](#${splitDat[i]
              .replace('## ', '')
              .replaceAll(' ', '-')
              .replaceAll('(', '')
              .replaceAll(')', '')
              .replaceAll('!', '')
              .replaceAll('.', '')
              .replace(/[^a-zA-Z0-9]/g, '-')
              .replaceAll('--', '-')
              .toLowerCase()})\n`;
          }
        }
      } catch (__) {}

      data = md
        .render(toc + '\n' + data)
        .replaceAll('<li', '<li class="li"')
        .replaceAll('<ul', '<ul class="ul"')
        .replaceAll('<button', '<button class="button-quail"')
        .replaceAll('<textarea', '<textarea class="fform"')
        .replaceAll('<h2', '<h2 class="h2"')
        .replaceAll('<h3', '<h3 class="h3"')
        .replaceAll('<blockquote', '<blockquote class="blockquote"')
        .replaceAll('<table', '<table class="table"')
        .replaceAll('<thead', '<thead class="thead"')
        .replaceAll('<tr', '<tr class="tr"');

      return {
        props: {
          data: data,
          perms: await perms.json(),
          js: js,
          path: params.route.split('/')
        }
      };
    } else {
      return {
        status: res.status,
        error: new Error(`Could not load ${url}`)
      };
    }
  }
</script>

<script lang="ts">
  import QuailTree from '../_helpers/QuailTree.svelte';
  import { browser } from '$app/env';
  import { lynxUrl, apiUrl, electroUrl } from '$lib/config';

  export let data: any;
  export let js: string;
  export let path: string[];
  export let perms: any;

  function title(str) {
    return str
      .replaceAll('-', ' ')
      .replaceAll('_', ' ')
      .replace(/(^|\s)\S/g, function (t) {
        return t.toUpperCase();
      });
  }

  if (browser) {
    let script = document.createElement('script');
    script.innerHTML = js;
    document.body.appendChild(script);
  }

  js = js;
</script>

<QuailTree perms={perms.perm}>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.4.0/build/styles/a11y-dark.min.css"
  />
  <div class="docs-quail">
    <h1>{title(path[path.length - 1].replaceAll('-', ' '))}</h1>
    {@html data}
    {@html '<' + 'script>' + js + '</script>'}
  </div>
</QuailTree>

<style lang="scss">
  @import '../_helpers/_hl.css';
</style>
