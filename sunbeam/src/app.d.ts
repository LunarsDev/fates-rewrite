/// <reference types="@sveltejs/kit" />

export {};

interface UserInterface {
  id: string;
  username: string;
  disc: string;
  avatar: string;
}

interface PageData {
  user: UserInterface;
  token: string;
  css: string?;
  refresh_token: string?;
  user_experiments: number[];
  site_lang: string;
}

interface UserFnInterface {
  id: string;
  token: string;
  apiUrl: string;
}

declare global {
  namespace App {
    interface Permission {
      index: number;
      roles: string[];
      name: string;
    }

    interface PageData {
      user: UserInterface;
      token: string;
      css: string?;
      refresh_token: string?;
      user_experiments: number[];
      site_lang: string;
      url: string;
      allowBanned: boolean; // Whether or not the user was allowed to do this action despite being banned
      permissions: Permission;
    }

    interface Error {
      message: string;
    }
  }

  namespace globalThis {
    interface Window {
      user: () => UserFnInterface;
      llhandler: () => void;

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      QuillMarkdown: any;
    }
  }
}
