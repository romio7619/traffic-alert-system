import sys
sys.path.append('..')
from event_bus import IEventSubscriber

class LoggingService(IEventSubscriber):
    def __init__(self):
        self.seen_ids = set()
        self.logs = []

    def handle(self, envelope):
        if envelope.event_id in self.seen_ids:
            print(f"[LoggingService] DUPLICATE BLOCKED: {envelope.event_id}")
            return

        self.seen_ids.add(envelope.event_id)
        log_entry = {
            "event_id": envelope.event_id,
            "event_type": envelope.event_type,
            "source": envelope.source_id,
            "time": envelope.timestamp,
            "payload": envelope.payload
        }
        self.logs.append(log_entry)
        print(f"[LoggingService] Logged: {envelope.event_type} from {envelope.source_id}")