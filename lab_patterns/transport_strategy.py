from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Trip:
    """Поездка, для которой считаем стоимость билета/проезда."""
    distance_km: float          # расстояние, км
    time_of_day: str = "day"    # "day" или "night"
    zones: int = 1              # количество зон (актуально для метро, электрички)


class TransportStrategy(ABC):
    """Базовый класс стратегии расчёта стоимости."""

    @abstractmethod
    def calculate_price(self, trip: Trip) -> float:
        """Вернуть стоимость поездки в рублях."""


class BusStrategy(TransportStrategy):
    """Автобус: 40 руб + 3 руб/км"""
    def calculate_price(self, trip: Trip) -> float:
        base_price = 40.0
        per_km = 3.0
        price = base_price + trip.distance_km * per_km
        return round(price, 2)


class MetroStrategy(TransportStrategy):
    """Метро: 55 руб за 1 зону, +20 руб за каждую следующую"""
    def calculate_price(self, trip: Trip) -> float:
        base_zone_price = 55.0
        extra_zone_price = 20.0
        if trip.zones <= 1:
            price = base_zone_price
        else:
            price = base_zone_price + (trip.zones - 1) * extra_zone_price
        return round(price, 2)


class TaxiStrategy(TransportStrategy):
    """Такси: 100 руб подача + 15 руб/км, ночью +20%"""
    def calculate_price(self, trip: Trip) -> float:
        base = 100.0
        per_km = 15.0
        price = base + trip.distance_km * per_km

        if trip.time_of_day == "night":
            price *= 1.2  # +20%

        return round(price, 2)


class TicketCalculator:
    """Контекст: использует выбранную стратегию."""
    def __init__(self, strategy: TransportStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: TransportStrategy) -> None:
        self._strategy = strategy

    def calculate(self, trip: Trip) -> float:
        return self._strategy.calculate_price(trip)


# Паттерн "Декоратор" для стратегий

class PriceDecorator(TransportStrategy):
    """
    Базовый декоратор.
    Реализует тот же интерфейс, что и стратегия, и хранит внутри "обёрнутую" стратегию.
    """

    def __init__(self, wrapped: TransportStrategy):
        self._wrapped = wrapped

    def calculate_price(self, trip: Trip) -> float:
        # По умолчанию просто передаёт вызов внутрь
        return self._wrapped.calculate_price(trip)


class CommissionDecorator(PriceDecorator):
    """
    Декоратор, добавляющий фиксированную наценку к цене (например, комиссию сервиса).
    """

    def __init__(self, wrapped: TransportStrategy, commission: float):
        super().__init__(wrapped)
        self._commission = commission

    def calculate_price(self, trip: Trip) -> float:
        base_price = super().calculate_price(trip)
        return base_price + self._commission


class DiscountDecorator(PriceDecorator):
    """
    Декоратор, уменьшающий цену на заданный процент (скидка, промокод и т.п.).
    """

    def __init__(self, wrapped: TransportStrategy, percent: float):
        super().__init__(wrapped)
        self._percent = percent

    def calculate_price(self, trip: Trip) -> float:
        base_price = super().calculate_price(trip)
        return base_price * (1 - self._percent / 100.0)


