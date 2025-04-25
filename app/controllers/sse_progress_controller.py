from flask import Blueprint, Response, request, stream_with_context
import time

sse_progress_bp = Blueprint('sse_progress_bp', __name__)

# In-memory progress store: {session_id: {"total": int, "done": int}}
# For production, use Redis or DB!
progress_store = {}

@sse_progress_bp.route('/progress/stream')
def progress_stream():
    session_id = request.args.get("session_id")
    if not session_id:
        return Response("Missing session_id", status=400)
    def event_stream():
        last_done = -1
        while True:
            prog = progress_store.get(session_id, {"total": 1, "done": 0})
            if prog["done"] != last_done:
                yield f"data: {prog['done']},{prog['total']}\n\n"
                last_done = prog["done"]
            if prog["done"] >= prog["total"]:
                break
            time.sleep(1)
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")