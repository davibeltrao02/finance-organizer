from app.handlers.transaction import TransactionHandler
from app.handlers.summary import SummaryHandler
from app.handlers.unknown import UnknownHandler

INTENT_HANDLERS = {
    "transaction": TransactionHandler(),
    "summary": SummaryHandler(),
    "unknown": UnknownHandler(),
}
