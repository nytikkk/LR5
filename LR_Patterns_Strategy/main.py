
from lab_patterns.transport_strategy import (
    Trip,
    TicketCalculator,
    BusStrategy,
    MetroStrategy,
    TaxiStrategy,
)


def main():
    # Одна и та же поездка
    trip = Trip(distance_km=10, time_of_day="day", zones=2)

    print("Поездка:", trip)

    calculator = TicketCalculator(BusStrategy())
    print("Автобус:", calculator.calculate(trip), "руб.")

    calculator.set_strategy(MetroStrategy())
    print("Метро:", calculator.calculate(trip), "руб.")

    calculator.set_strategy(TaxiStrategy())
    print("Такси (днём):", calculator.calculate(trip), "руб.")

    night_trip = Trip(distance_km=10, time_of_day="night", zones=2)
    print("\nНочная поездка:", night_trip)

    calculator.set_strategy(TaxiStrategy())
    print("Такси (ночью):", calculator.calculate(night_trip), "руб.")


if __name__ == "__main__":
    main()
