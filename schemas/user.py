from pydantic import BaseModel, Field


class UserData(BaseModel):
    id: int = Field(
        title="User ID",
        description="Discord user id"
    )
    money: int = Field(
        default=0,
        title="Money",
        description="Money owned by the user"
    )
    pancake: int = Field(
        default=0,
        title="Pancake",
        description="Pancake owned by the user"
    )
    bank_money: int = Field(
        default=0,
        title="Bank Money",
        description="Money stored in bank"
    )
    bank_limit: int = Field(
        default=1000,
        title="Bank Limit",
        description="User's bank limit"
    )
    experience: int = Field(
        default=0,
        title="Experience",
        description="User's experience"
    )
    stock: dict[str, int] = Field(
        default={},
        title="Stock",
        description="Stock owned by the user, key is stock id and value is count"
    )
    mining_time: int = Field(
        default=0,
        title="Mining Time",
        description="Timestamp when user start mining"
    )
