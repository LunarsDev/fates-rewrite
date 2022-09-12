import { writable } from 'svelte/store';

type LoadStore = string;

export default writable<LoadStore>(null);
