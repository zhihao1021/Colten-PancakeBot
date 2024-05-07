from fastapi import Depends

from typing import Annotated

from config import (
    OAUTH_JWT_KEY,
    OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET,
    OAUTH_REDIRECT_URI,
)
from discord_oauth import DiscordOAuthRouter, JWTData

discord_oauth_router = DiscordOAuthRouter(
    redirect_uri=OAUTH_REDIRECT_URI,
    client_id=OAUTH_CLIENT_ID,
    client_secret=OAUTH_CLIENT_SECRET,
    key=OAUTH_JWT_KEY,
)

user_depends = Depends(discord_oauth_router.valid_token)
UserDepends = Annotated[JWTData, user_depends]
