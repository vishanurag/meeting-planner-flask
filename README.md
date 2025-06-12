
# Smart Meeting Planner – Reflection

## _Note_
- I don't have that much knowledge about working with Flask or Fast API in python. 
- But somehow I challeged myself to learn Flask & develop this project via following some youtube tutorials & asking ChatGPT for code snippets & debugging my code. 
- Also learnt about various stuff while working on this project such as:

  
  1. Creating Flask server.
  2. Learnt how to use `Api` class other that using `@app.route()` python decorator.
  3. Understanding about CORS & resolving them.
  4. Testing the flask Apis using Postman.
   

## 1. How exactly did you use AI while building this?  
**Tools Used: (Not only limited to AI)**
- **ChatGPT (OpenAI)**: For Flask API design, CORS error debugging, frontend code generation, and JSON parsing logic.
- **Google**: Used google search for searching for various code snippets & ways to develop apis.
- **Youtube (Dave Gray & Network Chuck)**: Learnt how to work with flask.

**Prompts Given:**
- “Flask REST API for accepting busy slots and suggesting meeting times”
- “How to resolve CORS error between Flask and frontend on 127.0.0.1”
- “Bootstrap UI for submitting JSON, getting time suggestions, and booking meetings”
- “Fix internal server error with list object has no attribute 'split'”
- “How to parse nested JSON in reqparse”

**Successes:**
- Was able to quickly scaffold the entire Flask backend, including parsing complex input structures.
- Generated a fully functional frontend using only Bootstrap and basic JS.
- AI helped understand the cause of multiple Flask issues (e.g., CORS, type parsing).

**Failures:**
- Initial prompts caused confusion with `reqparse` parsing lists (which didn't work out of the box).
- AI initially suggested using `@marshal_with`, which conflicted with custom JSON response formatting.
- CORS issue required multiple iterations and testing; early responses weren’t fully effective until corrected.

---

## 2. If given two more days, what would you refactor or add first, and why?

If I had two more days:
- **Refactor Backend Logic**: Move slot parsing, availability computation, and booking logic into separate utility classes or services for cleaner code separation and testability.
- **Add Persistent Storage**: Right now, everything is in-memory. I’d integrate SQLite or PostgreSQL so data is not lost on server restart.
- **User Interface Enhancements**: Add a calendar UI (e.g., FullCalendar.js) so users can visually see busy/free slots instead of typing JSON manually.
- **Validation & Error Handling**: More robust feedback for invalid input, booking conflicts, or wrong user IDs.

These changes would make the app more production-ready and user-friendly.

## Repo Structure:

    backend📁
        api.py🔤 (source code)
        venv📁
    frontend📁
        index.html🔤 (source code)

## Local Setup:
- Backend Setup
    1. Navigate to backend📁 folder (cd backend).
    2. Run venv command (venv/Scripts/activate)
- Frontend Setup
    1. Navigate to frontend📁 folder (cd frontend).
    2. Run index.html file.
    