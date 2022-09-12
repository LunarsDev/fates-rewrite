enum BotState {
  approved = 0,
  pending = 1,
  denied = 2,
  hidden = 3,
  banned = 4,
  under_review = 5,
  certified = 6,
  archived = 7,
  private_viewable = 8,
  private_staff_only = 9
}

enum UserState {
  normal = 0,
  global_ban = 1,
  profile_edit_ban = 2,
  ddr_ban = 3, // Unused
  api_ban = 4 // Unused
}

enum UserFlags {
  Unknown = 0,
  VotesPrivate = 1,
  Staff = 2,
  AvidVoter = 3,
  Premium = 4
}

// This only covers site-supported user experiments
enum UserExperiments {
  Unknown = 0,
  GetRolesSelector = 1,
  LynxExperimentRolloutView = 2,
  BotReport = 3,
  ServerAppealCertification = 4,
  VotePrivacy = 5,
  DevPortal = 6
}

enum UserBotAction {
  approve = 0,
  deny = 1,
  certify = 2,
  ban = 3,
  claim = 4,
  unclaim = 5,
  transfer_ownership = 6,
  edit_bot = 7,
  delete_bot = 8,
  unban = 9,
  uncertify = 10,
  unverify = 11,
  requeue = 12
}

enum ReviewType {
  bot = 0,
  server = 1
}

enum CommandType {
  regular = 0,
  guild_slash = 1,
  global_slash = 2
}

enum Flag {
  unlocked = 0,
  edit_locked = 1,
  staff_locked = 2,
  stats_locked = 3,
  vote_locked = 4,
  system = 5,
  whitelist_only = 6,
  keep_banner_decor = 7,
  nsfw = 8
}

enum PageStyle {
  tabs = 0,
  single_view = 1
}

// Alert Types
export enum AlertType {
  Error = 1,
  Warning = 2,
  Info = 3,
  Alert = 4,
  Success = 5,
  Debug = 6,
  Prompt = 7
}

export enum AlertInputType {
  Text = 1,
  Number = 2,
  Boolean = 3,
  DateTime = 4,
  DateTimeLocal = 5,
  Color = 6,
  File = 7,
  Pre = 8 // Implements a metadata html element that can be put before another input
}

export const enums = {
  BotState: BotState,
  UserState: UserState,
  UserBotAction: UserBotAction,
  CommandType: CommandType,
  ReviewType: ReviewType,
  PageStyle: PageStyle,
  AlertType: AlertType,
  AlertInputType: AlertInputType,
  Flags: Flag,
  UserFlags: UserFlags,
  UserExperiments: UserExperiments,
  LongDescType: {
    html: 0,
    markdown_server: 1
  },
  helpers: {
    flagCheck: function (flags: number[] | number, allFlags: number[]) {
      // Function start
      let flagsParsed: number[] = [];
      if (typeof flags === 'number') {
        flagsParsed.push(flags);
      } else {
        flagsParsed = flags;
      }

      return flagsParsed.some((item) => allFlags.includes(item));
      // End of function
    }
  }
};
