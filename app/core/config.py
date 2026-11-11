"""Prices, container sizes, and coverage used to quote a paint job.

Override any field with an environment variable prefixed by ``PAINT_``,
for example ``PAINT_CAN_PRICE=30``.
"""

from decimal import Decimal
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Defaults match common Brazilian retail cans (3.6 L) and gallons (18 L)."""

    can_liters: Decimal = Field(default=Decimal("3.6"), gt=0)
    can_price: Decimal = Field(default=Decimal("25.00"), gt=0)
    gallon_liters: Decimal = Field(default=Decimal("18"), gt=0)
    gallon_price: Decimal = Field(default=Decimal("80.00"), gt=0)
    coverage_sqm_per_liter: Decimal = Field(default=Decimal("6"), gt=0)
    safety_margin_percent: Decimal = Field(default=Decimal("20"), ge=0)

    model_config = SettingsConfigDict(env_prefix="PAINT_", extra="ignore", frozen=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
