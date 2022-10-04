import { writable } from 'svelte/store';

interface MenuStore {
  open: string;
}

export default writable<MenuStore>({ open: '' });

export const errorStore = writable<MenuStore>({ open: '' });
