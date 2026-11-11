from decimal import Decimal

import pytest

from app.core.calculator import calculate_quote
from app.core.config import Settings


def test_three_purchase_options_for_a_typical_room():
    quote = calculate_quote(Decimal("100"), Settings())

    assert quote.area_sqm == Decimal("100")
    assert quote.area_with_margin_sqm == Decimal("120")
    assert quote.liters_needed == Decimal("20")

    assert quote.only_cans.cans == 6
    assert quote.only_cans.gallons == 0
    assert quote.only_cans.liters_purchased == Decimal("21.6")
    assert quote.only_cans.leftover_liters == Decimal("1.6")
    assert quote.only_cans.total_price == Decimal("150.00")

    assert quote.only_gallons.cans == 0
    assert quote.only_gallons.gallons == 2
    assert quote.only_gallons.liters_purchased == Decimal("36")
    assert quote.only_gallons.total_price == Decimal("160.00")

    assert quote.optimized.cans == 1
    assert quote.optimized.gallons == 1
    assert quote.optimized.liters_purchased == Decimal("21.6")
    assert quote.optimized.total_price == Decimal("105.00")


def test_exact_can_multiple_has_no_leftover():
    # 18 m² with a 20% margin at 6 m²/L needs exactly one 3.6 L can.
    quote = calculate_quote(Decimal("18"), Settings())

    assert quote.liters_needed == Decimal("3.6")
    assert quote.only_cans.cans == 1
    assert quote.only_cans.leftover_liters == Decimal("0")
    assert quote.only_cans.total_price == Decimal("25.00")
    assert quote.only_gallons.gallons == 1
    assert quote.only_gallons.total_price == Decimal("80.00")
    assert quote.optimized.cans == 1
    assert quote.optimized.gallons == 0
    assert quote.optimized.total_price == Decimal("25.00")


def test_exact_gallon_multiple_prefers_the_gallon():
    # 90 m² with a 20% margin at 6 m²/L needs exactly 18 L.
    quote = calculate_quote(Decimal("90"), Settings())

    assert quote.liters_needed == Decimal("18")
    assert quote.only_cans.cans == 5
    assert quote.only_cans.leftover_liters == Decimal("0")
    assert quote.only_cans.total_price == Decimal("125.00")
    assert quote.only_gallons.gallons == 1
    assert quote.only_gallons.leftover_liters == Decimal("0")
    assert quote.only_gallons.total_price == Decimal("80.00")
    assert quote.optimized.cans == 0
    assert quote.optimized.gallons == 1
    assert quote.optimized.total_price == Decimal("80.00")


def test_zero_area_buys_nothing():
    quote = calculate_quote(Decimal("0"), Settings())

    assert quote.area_with_margin_sqm == Decimal("0")
    assert quote.liters_needed == Decimal("0")
    for purchase in (quote.only_cans, quote.only_gallons, quote.optimized):
        assert purchase.cans == 0
        assert purchase.gallons == 0
        assert purchase.liters_purchased == Decimal("0")
        assert purchase.leftover_liters == Decimal("0")
        assert purchase.total_price == Decimal("0.00")


def test_negative_area_is_rejected():
    with pytest.raises(ValueError, match="area_sqm"):
        calculate_quote(Decimal("-1"), Settings())


def test_optimized_prefers_cans_when_gallons_cost_more():
    settings = Settings(gallon_price=Decimal("200"))
    quote = calculate_quote(Decimal("90"), settings)

    assert quote.optimized.cans == 5
    assert quote.optimized.gallons == 0
    assert quote.optimized.total_price == Decimal("125.00")


def test_optimized_buys_another_gallon_when_extra_cans_cost_more():
    # 29 L is more than one gallon. Four cans for the remainder cost more
    # than simply buying a second gallon.
    quote = calculate_quote(Decimal("145"), Settings())

    assert quote.liters_needed == Decimal("29")
    assert quote.only_cans.total_price == Decimal("225.00")
    assert quote.only_gallons.gallons == 2
    assert quote.only_gallons.total_price == Decimal("160.00")
    assert quote.optimized.cans == 0
    assert quote.optimized.gallons == 2
    assert quote.optimized.total_price == Decimal("160.00")


def test_zero_safety_margin_uses_the_raw_area():
    settings = Settings(safety_margin_percent=Decimal("0"))
    quote = calculate_quote(Decimal("60"), settings)

    assert quote.area_with_margin_sqm == Decimal("60")
    assert quote.liters_needed == Decimal("10")
    assert quote.optimized.cans == 3
    assert quote.optimized.gallons == 0
    assert quote.optimized.total_price == Decimal("75.00")


@pytest.mark.parametrize(
    "area",
    [Decimal("0"), Decimal("1"), Decimal("18"), Decimal("90"), Decimal("100"), Decimal("145")],
)
def test_optimized_is_never_more_expensive_than_a_single_size(area):
    quote = calculate_quote(area, Settings())

    assert quote.optimized.total_price <= quote.only_cans.total_price
    assert quote.optimized.total_price <= quote.only_gallons.total_price


def test_configured_coverage_changes_liters():
    settings = Settings(coverage_sqm_per_liter=Decimal("10"), safety_margin_percent=Decimal("0"))
    quote = calculate_quote(Decimal("36"), settings)

    assert quote.liters_needed == Decimal("3.6")
    assert quote.optimized.cans == 1
    assert quote.optimized.total_price == Decimal("25.00")
