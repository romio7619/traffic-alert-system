import sys
sys.path.append('..')
from event_bus import IEventSubscriber

class AlertService(IEventSubscriber):
    def __init__(self):
        self.seen_ids = set()
        self.penalties_sent = 0
        self.blocked_duplicates = 0

    def handle(self, envelope):
        # IDEMPOTENCY CHECK — blocks duplicate events
        if envelope.event_id in self.seen_ids:
            print(f"[AlertService] DUPLICATE BLOCKED: {envelope.event_id}")
            self.blocked_duplicates += 1
            return

        self.seen_ids.add(envelope.event_id)
        payload = envelope.payload
        event_type = envelope.event_type

        if event_type == "SpeedViolationEvent":
            print(f"[AlertService] Speed penalty issued to: {payload.get('vehicle_plate')} | {payload.get('speed')} km/h")
            self.penalties_sent += 1

        elif event_type == "WrongWayDriverEvent":
            print(f"[AlertService] Wrong-way penalty issued to: {payload.get('vehicle_plate')} | {payload.get('direction')}")
            self.penalties_sent += 1