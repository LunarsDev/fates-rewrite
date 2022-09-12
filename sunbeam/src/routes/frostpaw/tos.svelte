<script context="module" lang="ts">
  export const prerender = false;
  import { fetchFates } from '$lib/request';
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    return {
      status: 301,
      redirect: `https://lynx.fateslist.xyz/privacy`
    };
  }
</script>
