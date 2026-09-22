import uuid
from datetime import datetime, timezone

class GovernanceService:
    def __init__(self):
        self.owner_id = "owner-001"
        self.requests = []

    def create_request(self, data):
        item = {
            "id": str(uuid.uuid4()),
            **data,
            "status": "PENDING",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "decided_at": None,
            "decided_by": None,
        }
        self.requests.append(item)
        return item

    def list_requests(self):
        return self.requests

    def decide(self, request_id, decision, owner_id):
        for item in self.requests:
            if item["id"] == request_id:
                item["status"] = decision
                item["decided_at"] = datetime.now(timezone.utc).isoformat()
                item["decided_by"] = owner_id
                return item
        raise KeyError("Agent request not found")

governance = GovernanceService()
