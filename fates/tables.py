from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import BigInt
from piccolo.columns.column_types import Boolean
from piccolo.columns.column_types import Array
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Interval
from piccolo.columns.column_types import JSONB
from piccolo.columns.column_types import Numeric
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamptz
from piccolo.columns.column_types import UUID
from piccolo.columns.defaults.interval import IntervalCustom
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.columns.defaults.uuid import UUID4
from piccolo.table import Table
from decimal import Decimal
import secrets
from fates import enums


class Bots(Table, tablename="bots"):
    bot_id = BigInt(
        default=0,
        null=False,
        primary_key=True,
        unique=True,
        index=True,
        secret=False,
    )
    extra_links = JSONB(
        nullable=False,
        default={},
        help_text="Extra links to be displayed in the bot's page",
    )
    votes = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    guild_count = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    shard_count = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    library = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    webhook = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    description = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    long_description = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    prefix = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    banner_card = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    created_at = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    invite = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    features = Array(
        null=True,
        base_column=Text(),
        primary_key=False,
        unique=False,
        secret=False,
    )
    invite_amount = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_count = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    css = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    shards = Array(
        base_column=Integer(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    username_cached = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    state = Integer(
        default=1,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    long_description_type = Integer(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    verifier = BigInt(
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    last_stats_post = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    webhook_type = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    api_token = Text(
        null=False,
        default=secrets.token_urlsafe(512),
        primary_key=False,
        unique=False,
    )
    webhook_secret = Text(
        null=False,
        default=secrets.token_urlsafe(512),
        primary_key=False,
        unique=False,
    )
    banner_page = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    total_votes = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    client_id = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    flags = Array(
        base_column=Integer(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    uptime_checks_total = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    uptime_checks_failed = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    page_style = Integer(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    webhook_hmac_only = Boolean(
        default=False,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    last_updated_at = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class BotListTags(Table, tablename="bot_list_tags"):
    id = Text(
        default="",
        null=False,
        primary_key=True,
        unique=True,
        index=True,
        secret=False,
    )
    icon = Text(
        default="",
        null=False,
        primary_key=False,
        unique=True,
        index=True,
        secret=False,
    )


class BotPacks(Table, tablename="bot_packs"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        index=True,
        secret=False,
    )
    icon = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    banner = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    owner = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    bots = Array(
        base_column=BigInt(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    description = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    name = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    created_at = Timestamptz(
        default=TimestamptzNow(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class BotStatsVotesPm(Table, tablename="bot_stats_votes_pm"):
    bot_id = BigInt(
        default=0,
        null=True,
        primary_key=True,
        unique=False,
        secret=False,
    )
    votes = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    epoch = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class Users(Table, tablename="users"):
    id = BigInt(
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    user_id = BigInt(
        null=False,
        primary_key=False,
        unique=True,
        secret=False,
    )
    api_token = Text(
        null=False,
        default=secrets.token_urlsafe(512),
        primary_key=False,
        unique=False,
    )
    description = Text(
        default="This user prefers to be an enigma",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    badges = Array(
        null=True,
        primary_key=False,
        unique=False,
        base_column=Text(),
        secret=False,
    )
    username = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_css = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    state = Integer(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    coins = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    site_lang = Text(
        default="default",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    profile_css = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    vote_reminders = Array(
        null=False,
        primary_key=False,
        unique=False,
        base_column=BigInt(),
        secret=False,
    )
    vote_reminder_channel = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    staff_verify_code = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    vote_reminders_last_acked = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    vote_reminders_servers = Array(
        null=False,
        primary_key=False,
        unique=False,
        base_column=BigInt(),
        secret=False,
    )
    vote_reminders_servers_last_acked = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    vote_reminder_servers_channel = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    experiments = Array(
        null=False,
        primary_key=False,
        unique=False,
        base_column=Integer(),
        secret=False,
    )
    flags = Array(
        null=False,
        primary_key=False,
        unique=False,
        base_column=Integer(),
        secret=False,
    )
    extra_links = JSONB(
        nullable=False,
        default={},
        help_text="Extra links to be displayed in the bot's page",
    )


class WsEvents(Table, tablename="ws_events"):
    id = BigInt(
        default=0,
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    type = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    ts = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    event = JSONB(
        default="{}",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class BotEvents(Table, tablename="bot_events"):
    id = UUID(
        default=UUID4(),
        primary_key=True,
    )
    bot_id = ForeignKey(
        references=Bots,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    event_type = Integer(
        choices=enums.EventType,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )

    ts = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )

    reason = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )

    css = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class Features(Table, tablename="features"):
    id = Text(
        default="",
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    name = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    description = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    viewed_as = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class FrostpawClient(Table, tablename="frostpaw_clients"):
    id = Text(
        primary_key=True, default=lambda: secrets.token_urlsafe().replace(".", "")
    )

    name = Text(
        null=False,
    )

    domain = Text(
        null=False,
    )

    privacy_policy = Text(
        null=False,
    )

    secret = Text(null=False, default=secrets.token_urlsafe)

    owner_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        target_column="user_id",
        on_update=OnUpdate.cascade,
        null=False,
    )

    verified = Boolean(
        default=False,
        null=False,
    )


class UserConnection(Table, tablename="user_connections"):
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        null=True,
        primary_key=True,
    )

    client_id = Text(null=False)

    refresh_token = Text(null=False)

    expires_on = Timestamptz(null=False, default=TimestamptzNow())


class LeaveOfAbsence(Table, tablename="leave_of_absence"):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    reason = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    estimated_time = Interval(
        default=IntervalCustom(
            weeks=0,
            days=0,
            hours=0,
            minutes=0,
            seconds=0,
            milliseconds=0,
            microseconds=0,
        ),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    start_date = Timestamptz(
        default=TimestamptzNow(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_id = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class LynxData(Table, tablename="lynx_data"):
    default_user_experiments = Array(
        base_column=Integer(),
        help_text="Do not modify this if you do not know what you are doing",
    )


class LynxNotifications(Table, tablename="lynx_notifications"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    acked_users = Array(
        base_column=BigInt(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    message = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    type = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    staff_only = Boolean(
        default=False,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class LynxSurveys(Table, tablename="lynx_surveys"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        index=True,
        secret=False,
    )
    title = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    questions = JSONB(
        default="{}",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    created_at = Timestamptz(
        default=TimestamptzNow(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class PlatformMap(Table, tablename="platform_map"):
    fates_id = Numeric(
        default=Decimal("0"),
        digits=None,
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    platform_id = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class ServerTags(Table, tablename="server_tags"):
    id = Text(
        default="",
        null=False,
        primary_key=True,
        unique=True,
        index=True,
        secret=False,
    )
    name = Text(
        default="",
        null=False,
        primary_key=False,
        unique=True,
        index=True,
        secret=False,
    )
    owner_guild = BigInt(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    iconify_data = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class Vanity(Table, tablename="vanity"):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    type = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    vanity_url = Text(
        default="",
        null=True,
        primary_key=False,
        unique=True,
        index=True,
        secret=False,
    )
    redirect = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=True,
        index=True,
        secret=False,
    )


class BotCommands(Table, tablename="bot_commands"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    bot_id = ForeignKey(
        references=Bots,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    cmd_type = Integer(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    groups = Array(
        base_column=Text(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    name = Text(
        default="",
        null=False,
        primary_key=True,
        unique=True,
        index=True,
        secret=False,
    )
    vote_locked = Boolean(
        default=False,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    description = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    args = Array(
        base_column=Text(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    examples = Array(
        base_column=Text(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    premium_only = Boolean(
        default=False,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    notes = Array(
        base_column=Text(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    doc_link = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    nsfw = Boolean(
        default=False,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class BotOwner(Table, tablename="bot_owner"):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    bot_id = ForeignKey(
        references=Bots,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    owner = BigInt(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    main = Boolean(
        default=False,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class BotTags(Table, tablename="bot_tags"):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    bot_id = ForeignKey(
        references=Bots,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    tag = ForeignKey(
        references=BotListTags,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class BotVoters(Table, tablename="bot_voters"):
    bot_id = BigInt(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    timestamps = Array(
        base_column=Timestamptz(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class LynxApps(Table, tablename="lynx_apps"):
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    app_id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        index=True,
        secret=False,
    )
    questions = JSONB(
        default="{}",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    answers = JSONB(
        default="{}",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    app_version = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    created_at = Timestamptz(
        default=TimestamptzNow(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class LynxRatings(Table, tablename="lynx_ratings"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    feedback = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    username_cached = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    page = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class Reviews(Table, tablename="reviews"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    target_id = BigInt(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    star_rating = Numeric(
        default=Decimal("0"),
        digits=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    review_text = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    flagged = Boolean(
        default=False,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    epoch = Array(
        null=False,
        primary_key=False,
        unique=False,
        base_column=BigInt(),
        secret=False,
    )
    target_type = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    parent_id = ForeignKey(
        references="self",
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class Servers(Table, tablename="servers"):
    guild_id = BigInt(
        null=False,
        primary_key=True,
        unique=True,
        secret=False,
    )
    votes = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    api_token = Text(
        null=False,
        default=secrets.token_urlsafe(512),
        primary_key=False,
        unique=False,
    )
    webhook = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    description = Text(
        default="No description set",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    long_description = Text(
        default="No long description set! Set one with /settings longdesc Long description",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    css = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    invite_amount = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    invite_url = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    name_cached = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    long_description_type = Integer(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    state = Integer(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    created_at = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    avatar_cached = Text(
        default="Unlisted",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    invite_channel = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    nsfw = Boolean(
        default=False,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    guild_count = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    banner_card = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    banner_page = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    webhook_type = Integer(
        default=1,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    login_required = Boolean(
        default=True,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    total_votes = BigInt(
        default=0,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    tags = Array(
        base_column=Text(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    owner_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    flags = Array(
        base_column=Integer(choices=enums.BotServerFlag),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    autorole_votes = Array(
        base_column=BigInt(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    whitelist_only = Boolean(
        default=False,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    whitelist_form = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    webhook_hmac_only = Boolean(
        default=False,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    old_state = Integer(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_whitelist = Array(
        base_column=BigInt(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_blacklist = Array(
        base_column=BigInt(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )

    extra_links = JSONB(
        nullable=False,
        default={},
        help_text="Extra links to be displayed in the bot's page",
    )


class ServerVoters(Table, tablename="server_voters"):
    guild_id = BigInt(
        default=0,
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    timestamps = Array(
        base_column=Timestamptz(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class UserBotLogs(Table, tablename="user_bot_logs"):
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    bot_id = BigInt(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    action_time = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    action = Integer(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    context = Text(
        default="",
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class UserServerVoteTable(Table, tablename="user_server_vote_table"):
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=True,
        unique=False,
        index=True,
        secret=False,
    )
    guild_id = BigInt(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    expires_on = Timestamptz(
        default=TimestamptzNow(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class UserVoteTable(Table, tablename="user_vote_table"):
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=True,
        unique=False,
        index=True,
        secret=False,
    )
    bot_id = BigInt(
        default=0,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    expires_on = Timestamptz(
        default=TimestamptzNow(),
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )


class LynxSurveyResponses(Table, tablename="lynx_survey_responses"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    questions = JSONB(
        default="{}",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    answers = JSONB(
        default="{}",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    username_cached = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=True,
        primary_key=False,
        unique=False,
        secret=False,
    )
    survey_id = ForeignKey(
        references=LynxSurveys,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class ReviewVotes(Table, tablename="review_votes"):
    id = ForeignKey(
        references=Reviews,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        target_column=None,
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    upvote = Boolean(
        default=False,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class ServerAuditLogs(Table, tablename="server_audit_logs"):
    action_id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        secret=False,
    )
    guild_id = ForeignKey(
        references=Servers,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    username = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    user_guild_perms = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    field = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    value = Text(
        default="",
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )
    action_time = Timestamptz(
        default=TimestamptzNow(),
        null=False,
        primary_key=False,
        unique=False,
        secret=False,
    )


class PushNotifications(Table, tablename="push_notifications"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
    )

    user_id = ForeignKey(
        references=Users,
        on_delete=OnDelete.cascade,
        on_update=OnUpdate.cascade,
        null=False,
    )

    endpoint = Text(
        null=False,
    )

    p256dh = Text(
        null=False,
    )

    auth = Text(
        null=False,
    )
