from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2022-09-12T16:31:48:455500"
VERSION = "0.90.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
