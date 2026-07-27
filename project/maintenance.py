"""
Maintenance routes - not part of the normal app functionality (for demo deployment only).

`/admin/reset-demo` is deliberately NOT protected by the usual `login_required` / `role_required` decorators in `decorators.py`, because the
caller here is an automated GitHub Actions job with no logged-in session - it's a machine-to-machine call, checked with a shared secret header instead.

Set `RESET_SECRET` as an environment variable in Render (and as a matching GitHub Actions secret) - never commit the actual value.
"""
from dotenv import load_dotenv
import os
from flask import Blueprint, request, jsonify
from project.reset import reset_demo_data

load_dotenv()         # load env variables

maintenance_bp = Blueprint("maintenance", __name__)

@maintenance_bp.route("/admin/reset-demo", methods=["POST"])
def reset_demo():
    expected = os.environ.get("RESET_SECRET")
    provided = request.headers.get("X-Reset-Key")

    if not expected:
        # Fails closed: if the secret isn't configured, refuse rather than silently allowing an unauthenticated reset.
        return jsonify({"error": "RESET_SECRET not configured"}), 500

    if provided != expected:
        return jsonify({"error": "forbidden"}), 403

    result = reset_demo_data()
    return jsonify(result), 200