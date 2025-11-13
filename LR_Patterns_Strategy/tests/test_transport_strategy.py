import unittest
from unittest.mock import Mock

from lab_patterns.transport_strategy import (
    Trip,
    BusStrategy,
    MetroStrategy,
    TaxiStrategy,
    TicketCalculator,
)


class TestTransportStrategies(unittest.TestCase):
    def setUp(self):
        # Одна базовая поездка для большинства тестов
        self.trip_day = Trip(distance_km=10, time_of_day="day", zones=2)
        self.trip_night = Trip(distance_km=10, time_of_day="night", zones=2)

    def test_bus_strategy(self):
        """Проверка формулы для автобуса: 40 + 3 * distance."""
        strategy = BusStrategy()
        price = strategy.calculate_price(self.trip_day)
        expected = 40 + 3 * 10
        self.assertAlmostEqual(price, expected, places=2)

    def test_metro_strategy_one_zone(self):
        """Метро с одной зоной — базовая цена."""
        trip = Trip(distance_km=0, time_of_day="day", zones=1)
        strategy = MetroStrategy()
        price = strategy.calculate_price(trip)
        expected = 55.0
        self.assertEqual(price, expected)

    def test_metro_strategy_multiple_zones(self):
        """Метро с несколькими зонами: 55 + 20*(zones-1)."""
        strategy = MetroStrategy()
        price = strategy.calculate_price(self.trip_day)  # zones=2
        expected = 55 + 20 * (2 - 1)
        self.assertEqual(price, expected)

    def test_taxi_strategy_day(self):
        """Такси днём: 100 + 15 * distance."""
        strategy = TaxiStrategy()
        price = strategy.calculate_price(self.trip_day)
        expected = 100 + 15 * 10
        self.assertAlmostEqual(price, expected, places=2)

    def test_taxi_strategy_night(self):
        """Такси ночью: (100 + 15 * distance) * 1.2."""
        strategy = TaxiStrategy()
        price = strategy.calculate_price(self.trip_night)
        expected = (100 + 15 * 10) * 1.2
        self.assertAlmostEqual(price, expected, places=2)

    def test_ticket_calculator_uses_strategy(self):
        """Проверяем, что TicketCalculator вызывает стратегию (mock)."""
        fake_strategy = Mock()
        fake_strategy.calculate_price.return_value = 999.99

        calculator = TicketCalculator(fake_strategy)
        trip = self.trip_day

        result = calculator.calculate(trip)

        # Результат должен быть именно тот, что вернул mock
        self.assertEqual(result, 999.99)
        # И mock должен быть вызван ровно один раз с нужным аргументом
        fake_strategy.calculate_price.assert_called_once_with(trip)


if __name__ == "__main__":
    unittest.main()

