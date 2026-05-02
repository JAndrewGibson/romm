from typing import NotRequired, TypedDict, get_type_hints

<<<<<<< HEAD
from pydantic import computed_field

from handler.metadata.ra_handler import RAUserProgression
from models.user import Role
=======
from pydantic import ConfigDict
from starlette.requests import Request
>>>>>>> upstream/master

from handler.metadata.ra_handler import RAUserProgression
from models.user import Role, User

from .base import BaseModel, UTCDatetime


RAProgression = TypedDict(  # type: ignore[misc]
    "RAProgression",
    {k: NotRequired[v] for k, v in get_type_hints(RAUserProgression).items()},  # type: ignore[misc]
    total=False,
)


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str | None
    enabled: bool
    role: Role
    oauth_scopes: list[str]
    avatar_path: str
    last_login: UTCDatetime | None
    last_active: UTCDatetime | None
    ra_username: str | None = None
    ra_progression: RAProgression | None = None
    ui_settings: dict | None = None
<<<<<<< HEAD
    playtime_tracking_enabled: bool = True
    friends_tab_visible: bool = True
=======
    current_device_id: str | None = None
>>>>>>> upstream/master

    created_at: UTCDatetime
    updated_at: UTCDatetime

    @classmethod
    def from_orm_with_request(
        cls, db_user: User | None, request: Request
    ) -> "UserSchema | None":
        if not db_user:
            return None

        schema = cls.model_validate(db_user)
        schema.current_device_id = request.session.get("device_id")
        return schema

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
