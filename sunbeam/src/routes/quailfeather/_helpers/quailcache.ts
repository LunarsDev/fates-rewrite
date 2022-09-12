import { writable } from 'svelte/store';

interface DocTreeInterface {
  treeDepthOne: string[];
  treeDepthTwo: any;
}

type DocTree = DocTreeInterface;

export const doctreeCache = writable<DocTree>(null);
