from datetime import datetime
from typing import NotRequired, TypedDict, get_type_hints

from pydantic import computed_field

from handler.metadata.ra_handler import RAUserProgression
from models.user import Role

from .base import BaseModel


RAProgression = TypedDict(  # type: ignore[misc]
    "RAProgression",
    {k: NotRequired[v] for k, v in get_type_hints(RAUserProgression).items()},  # type: ignore[misc]
    total=False,
)


class UserSchema(BaseModel):
    id: int
    username: str
    email: str | None
    enabled: bool
    role: Role
    oauth_scopes: list[str]
    avatar_path: str
    last_login: datetime | None
    last_active: datetime | None
    ra_username: str | None = None
    ra_progression: RAProgression | None = None
    ui_settings: dict | None = None
    playtime_tracking_enabled: bool = True
    friends_tab_visible: bool = True

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @computed_field  # type: ignore[misc]
    @property
    def avatar_url(self) -> str | None:
        if not self.avatar_path:
            return None
        return f"/assets/romm/assets/{self.avatar_path}?ts={int(self.updated_at.timestamp())}"


from endpoints.responses.rom import SimpleRomSchema


class InviteLinkSchema(BaseModel):
    token: str


class UserPlayedRomSchema(SimpleRomSchema):
    play_time_ms: int

class UserStatsSchema(BaseModel):
    total_play_time_ms: int
    top_played_roms: list[UserPlayedRomSchema]

class UserFriendSchema(UserSchema):
    recent_games: list[SimpleRomSchema] = []
    play_time_ms: int = 0
