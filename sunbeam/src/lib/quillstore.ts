import { writable } from 'svelte/store';

type QuillStore = Map<string, any>;

export default writable<QuillStore>(null);
