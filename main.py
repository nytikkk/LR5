
from lab_patterns.transport_strategy import (
    Trip,
    TicketCalculator,
    BusStrategy,
    MetroStrategy,
    TaxiStrategy,
    PriceDecorator,
    CommissionDecorator,
    DiscountDecorator,
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
       
    print("\n=== Пример работы паттерна 'Декоратор' ===")
    trip = Trip(distance_km=10, zones=2, time_of_day="day")

    # Обычный автобусный тариф
    base_strategy = BusStrategy()
    base_calc = TicketCalculator(base_strategy)
    base_price = base_calc.calculate(trip)
    print(f"Базовая цена (автобус): {base_price} руб")

    # Добавляем комиссию сервиса +10 руб
    with_commission = CommissionDecorator(base_strategy, commission=10)
    calc_commission = TicketCalculator(with_commission)
    price_with_commission = calc_commission.calculate(trip)
    print(f"С комиссией +10 руб: {price_with_commission} руб")

    # Добавляем скидку 50% поверх комиссии
    with_discount = DiscountDecorator(with_commission, percent=50)
    calc_discount = TicketCalculator(with_discount)
    price_with_discount = calc_discount.calculate(trip)
    print(f"С комиссией + скидкой 50%: {price_with_discount} руб")



if __name__ == "__main__":
    main()
