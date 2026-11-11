from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_defaults_match_retail_cans_and_gallons():
    settings = Settings()

    assert settings.can_liters == Decimal("3.6")
    assert settings.can_price == Decimal("25.00")
    assert settings.gallon_liters == Decimal("18")
    assert settings.gallon_price == Decimal("80.00")
    assert settings.coverage_sqm_per_liter == Decimal("6")
    assert settings.safety_margin_percent == Decimal("20")


def test_paint_env_prefix_overrides_a_price(monkeypatch):
    monkeypatch.setenv("PAINT_CAN_PRICE", "30")

    assert Settings().can_price == Decimal("30")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("can_liters", "0"),
        ("can_liters", "-1"),
        ("can_price", "0"),
        ("can_price", "-5"),
        ("gallon_liters", "0"),
        ("gallon_price", "-1"),
        ("coverage_sqm_per_liter", "0"),
        ("coverage_sqm_per_liter", "-2"),
        ("safety_margin_percent", "-0.1"),
    ],
)
def test_settings_reject_zero_and_negative_values(field, value):
    with pytest.raises(ValidationError):
        Settings(**{field: Decimal(value)})


def test_zero_safety_margin_is_allowed():
    assert Settings(safety_margin_percent=Decimal("0")).safety_margin_percent == Decimal("0")
