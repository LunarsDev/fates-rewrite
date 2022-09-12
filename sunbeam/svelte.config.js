import cfAdapter from '@sveltejs/adapter-cloudflare';
import nodeAdapter from '@sveltejs/adapter-node';
import preprocess from 'svelte-preprocess';

var adapter;

if (process.env.CF_PAGES) {
  adapter = cfAdapter;
} else {
  adapter = nodeAdapter;
}

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: preprocess({
    preserve: ['ld+json']
  }),

  kit: {
    adapter: adapter(),

    prerender: {
      default: false,
      enabled: false
    }
  }
};

export default config;
