import { writable } from 'svelte/store';

interface MenuStore {
  open: string;
}

export default writable<MenuStore>({ open: '' });

export let errorStore = writable<MenuStore>({ open: '' });
