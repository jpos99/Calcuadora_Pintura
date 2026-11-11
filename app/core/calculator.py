"""Pure helpers that turn a surface area into three paint purchases.

Nothing here prints or reads the environment. Pass a :class:`Settings`
instance (or the defaults it already carries) and read the result.
"""

from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal

from app.core.config import Settings

_CENTS = Decimal("0.01")


@dataclass(frozen=True)
class Purchase:
    """One way to cover the required liters."""

    cans: int
    gallons: int
    liters_needed: Decimal
    liters_purchased: Decimal
    total_price: Decimal

    @property
    def leftover_liters(self) -> Decimal:
        return self.liters_purchased - self.liters_needed


@dataclass(frozen=True)
class Quote:
    """Area, liters, and the three purchase options."""

    area_sqm: Decimal
    area_with_margin_sqm: Decimal
    liters_needed: Decimal
    only_cans: Purchase
    only_gallons: Purchase
    optimized: Purchase


def calculate_quote(area_sqm: Decimal, settings: Settings) -> Quote:
    """Price cans only, gallons only, and the cheapest mix of both.

    ``area_sqm`` may be zero, which buys nothing. A negative area raises
    ``ValueError``.
    """
    if area_sqm < 0:
        raise ValueError("area_sqm must be zero or positive")

    area_with_margin = area_sqm * (1 + settings.safety_margin_percent / Decimal(100))
    liters_needed = area_with_margin / settings.coverage_sqm_per_liter
    return Quote(
        area_sqm=area_sqm,
        area_with_margin_sqm=area_with_margin,
        liters_needed=liters_needed,
        only_cans=_purchase(
            liters_needed,
            cans=_units_needed(liters_needed, settings.can_liters),
            gallons=0,
            settings=settings,
        ),
        only_gallons=_purchase(
            liters_needed,
            cans=0,
            gallons=_units_needed(liters_needed, settings.gallon_liters),
            settings=settings,
        ),
        optimized=_cheapest_mix(liters_needed, settings),
    )


def _cheapest_mix(liters_needed: Decimal, settings: Settings) -> Purchase:
    """Try every gallon count that can cover the liters, filling the rest with cans.

    The winning plan is the lowest price. Equal prices keep the plan with
    less leftover paint, then the plan with fewer containers.
    """
    max_gallons = _units_needed(liters_needed, settings.gallon_liters)
    best = _purchase(
        liters_needed,
        cans=_units_needed(liters_needed, settings.can_liters),
        gallons=0,
        settings=settings,
    )
    for gallons in range(1, max_gallons + 1):
        remaining = liters_needed - (gallons * settings.gallon_liters)
        if remaining < 0:
            remaining = Decimal(0)
        candidate = _purchase(
            liters_needed,
            cans=_units_needed(remaining, settings.can_liters),
            gallons=gallons,
            settings=settings,
        )
        if _is_better(candidate, best):
            best = candidate
    return best


def _is_better(candidate: Purchase, incumbent: Purchase) -> bool:
    if candidate.total_price != incumbent.total_price:
        return candidate.total_price < incumbent.total_price
    if candidate.leftover_liters != incumbent.leftover_liters:
        return candidate.leftover_liters < incumbent.leftover_liters
    return (candidate.cans + candidate.gallons) < (incumbent.cans + incumbent.gallons)


def _purchase(
    liters_needed: Decimal,
    *,
    cans: int,
    gallons: int,
    settings: Settings,
) -> Purchase:
    liters_purchased = (cans * settings.can_liters) + (gallons * settings.gallon_liters)
    total_price = (cans * settings.can_price) + (gallons * settings.gallon_price)
    return Purchase(
        cans=cans,
        gallons=gallons,
        liters_needed=liters_needed,
        liters_purchased=liters_purchased,
        total_price=total_price.quantize(_CENTS, rounding=ROUND_HALF_UP),
    )


def _units_needed(liters: Decimal, size: Decimal) -> int:
    if liters <= 0:
        return 0
    return int((liters / size).to_integral_value(rounding=ROUND_CEILING))
