
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from handler.database.base_handler import sync_session
from models.rom import Rom, RomUser
from sqlalchemy import select, func

def check_mismatch(user_id):
    with sync_session.begin() as session:
        # Total from RomUser directly
        total = session.scalar(
            select(func.sum(RomUser.play_time_ms))
            .where(RomUser.user_id == user_id)
        ) or 0
        print(f"Total Playtime for user {user_id}: {total} ms")

        # Roms with playtime
        stmt = select(RomUser).where(RomUser.user_id == user_id, RomUser.play_time_ms > 0)
        ru_entries = session.scalars(stmt).all()
        print(f"User {user_id} has {len(ru_entries)} RomUser entries with playtime > 0")
        
        for ru in ru_entries:
            rom = session.get(Rom, ru.rom_id)
            if not rom:
                print(f"  CRITICAL: RomUser entry {ru.id} has rom_id {ru.rom_id} which does NOT exist!")
            else:
                print(f"  Rom ID: {rom.id}, Name: {rom.name}, Playtime: {ru.play_time_ms}")

if __name__ == "__main__":
    check_mismatch(1) # Assuming user 1
