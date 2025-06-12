from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})


api = Api(app)

# Global storage
user_data = {}

# Constants
WORK_START = datetime.strptime("09:00", "%H:%M")
WORK_END = datetime.strptime("18:00", "%H:%M")

# Convert ["09:00", "10:30"] → (datetime, datetime)
def parse_interval(pair):
    if not isinstance(pair, list) or len(pair) != 2:
        raise ValueError(f"Invalid interval: {pair}")
    start = datetime.strptime(pair[0], "%H:%M")
    end = datetime.strptime(pair[1], "%H:%M")
    return (start, end)

# Merge overlapping intervals
def merge_busy_times(busy_lists):
    all_busy = []
    for user_busy in busy_lists:
        for interval in user_busy:
            all_busy.append(parse_interval(interval))
    all_busy.sort()

    merged = []
    for start, end in all_busy:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

# Get free slots between busy intervals
def get_free_slots(merged_busy, duration_minutes):
    free_slots = []
    current = WORK_START

    for start, end in merged_busy:
        if (start - current).total_seconds() / 60 >= duration_minutes:
            free_slots.append((current, start))
        current = max(current, end)

    if (WORK_END - current).total_seconds() / 60 >= duration_minutes:
        free_slots.append((current, WORK_END))

    return free_slots[:3]

# Format result into "HH:MM-HH:MM"
def format_slots(slots):
    return [f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}" for s, e in slots]

# POST /slots
class Slots(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'users' not in data or not isinstance(data['users'], list):
            return {"error": "Invalid input. 'users' must be a list."}, 400

        for user in data['users']:
            if 'id' not in user or 'busy' not in user or not isinstance(user['busy'], list):
                return {"error": "Each user must have an 'id' and a list of 'busy' intervals"}, 400
            for interval in user['busy']:
                if not isinstance(interval, list) or len(interval) != 2:
                    return {"error": f"Invalid busy interval for user {user['id']}: {interval}"}, 400

        user_data['users'] = data['users']
        return {"message": "User busy slots stored successfully."}, 201

# GET /suggest?duration=30
class Suggest(Resource):
    def get(self):
        try:
            duration = request.args.get("duration", type=int)
            if not duration or duration <= 0:
                return {"error": "Invalid or missing 'duration' query parameter."}, 400

            if 'users' not in user_data or not user_data['users']:
                return {"error": "No user data found. POST to /slots/ first."}, 400

            busy_lists = [user['busy'] for user in user_data['users']]
            merged = merge_busy_times(busy_lists)
            free_slots = get_free_slots(merged, duration)
            return {"available_slots": format_slots(free_slots)}, 200

        except Exception as e:
            return {"error": f"Internal error: {str(e)}"}, 500


# Store newly booked meetings (for simplicity, not implementing POST booking yet)
booked_data = {}

class Calendar(Resource):
    def get(self, user_id):
        user_id = int(user_id)

        # Check if user exists
        if 'users' not in user_data or not user_data['users']:
            return {"error": "No user data found. POST to /slots/ first."}, 400

        # Find the user
        user = next((u for u in user_data['users'] if u['id'] == user_id), None)
        if not user:
            return {"error": f"User with ID {user_id} not found."}, 404

        # Get busy slots (from slots)
        busy = user['busy']

        # Get booked meetings (if any)
        booked = booked_data.get(user_id, [])

        return {
            "user_id": user_id,
            "busy": busy,
            "booked_meetings": booked
        }, 200


api.add_resource(Slots, '/slots/')
api.add_resource(Suggest, '/suggest/')
api.add_resource(Calendar, '/calendar/<int:user_id>')


@app.route('/')
def index():
    return {"message": "Welcome! Use /slots to POST and /suggest?duration=XX to GET free slots."}, 200

if __name__ == '__main__':
    app.run(debug=True)
