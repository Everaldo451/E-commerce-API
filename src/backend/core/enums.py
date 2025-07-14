from enum import Enum

class OrderStatus(Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    PROCESSING = 'PROCESSING'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    CANCELED = 'CANCELED'