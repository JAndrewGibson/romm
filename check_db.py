
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from handler.database.base_handler import sync_session
from models.rom import Rom, RomUser
from models.user import User
from sqlalchemy import select

def check_playtime():
    with sync_session.begin() as session:
        # Check all users
        users = session.scalars(select(User)).all()
        print("--- USERS ---")
        for u in users:
            print(f"ID: {u.id}, Username: {u.username}, Playtime Enabled: {u.playtime_tracking_enabled}")

        # Check all rom_user entries with playtime
        print("\n--- PLAYTIME ---")
        stmt = select(RomUser).where(RomUser.play_time_ms > 0)
        results = session.scalars(stmt).all()
        
        print(f"Found {len(results)} entries with playtime > 0")
        for res in results:
            rom = session.get(Rom, res.rom_id)
            print(f"User ID: {res.user_id}, Rom/Game: {rom.name if rom else 'Unknown'}, Playtime MS: {res.play_time_ms}")

if __name__ == "__main__":
    check_playtime()
