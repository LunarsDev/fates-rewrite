/**
 * Can be made globally available by placing this
 * inside `global.d.ts` and removing `export` keyword
 */
export interface Locals {
  userid: string;
}
export interface TagInterface {
  id: string;
  name: string;
  iconify_data: string;
  owner_guild: string;
}
