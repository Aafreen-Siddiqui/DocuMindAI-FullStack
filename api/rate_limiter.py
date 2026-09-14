import time
from collections import defaultdict
from threading import Lock


request_log = defaultdict(list)
rate_limit_lock = Lock()


def is_rate_limited(
    client_id: str,
    limit: int,
    window_seconds: int = 60
) -> bool:

    current_time = time.time()

    with rate_limit_lock:

        # Remove expired requests
        request_log[client_id] = [
            timestamp
            for timestamp in request_log[client_id]
            if current_time - timestamp < window_seconds
        ]

        recent_requests = request_log[client_id]

        # Reject if limit is reached
        if len(recent_requests) >= limit:
            print(
                f"RATE LIMIT BLOCKED: {client_id} "
                f"({len(recent_requests)}/{limit})"
            )
            return True

        # Record allowed request
        recent_requests.append(current_time)

        print(
            f"REQUEST ACCEPTED: {client_id} "
            f"({len(recent_requests)}/{limit})"
        )

        return False