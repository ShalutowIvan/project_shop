import enum
class State_order(enum.Enum):
    received = "Получен"
    not_received = "Не получен"


print(State_order.received.value)