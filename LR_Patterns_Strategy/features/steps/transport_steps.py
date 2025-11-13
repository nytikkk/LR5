from behave import given, when, then
from lab_patterns.transport_strategy import (
    Trip,
    TicketCalculator,
    BusStrategy,
    TaxiStrategy,
)


@given('поездка {distance} км, {zones} зон(ы), время "{time_of_day}"')
def step_given_trip(context, distance, zones, time_of_day):
    """
    Создаём объект поездки с заданным расстоянием, количеством зон и временем суток.
    Значения distance и zones приходят в виде строк, поэтому конвертируем.
    """
    distance = float(distance)   # <-- ВАЖНО: переводим в float
    zones = int(zones)           # <-- ВАЖНО: переводим в int
    context.trip = Trip(distance_km=distance,
                        zones=zones,
                        time_of_day=time_of_day)


@when('стоимость считается по стратегии "автобус"')
def step_when_bus(context):
    """
    Считаем стоимость по автобусной стратегии.
    """
    calc = TicketCalculator(BusStrategy())
    context.price = calc.calculate(context.trip)


@when('стоимость считается по стратегии "такси"')
def step_when_taxi(context):
    """
    Считаем стоимость по стратегии такси.
    """
    calc = TicketCalculator(TaxiStrategy())
    context.price = calc.calculate(context.trip)


@then('стоимость должна быть {expected} руб')
def step_then_price(context, expected):
    """
    Проверяем, что рассчитанная цена соответствует ожидаемой.
    expected тоже приходит строкой, конвертируем в float.
    """
    expected = float(expected)
    actual = round(context.price, 2)
    assert actual == expected, f"Ожидали {expected}, а получили {actual}"
