import re
from flask import Flask, request, Response, redirect
from flask_cors import CORS
from youtube_dl import YoutubeDL
import json

ytdl = YoutubeDL({"outtmpl": "%(id)s%(ext)s"})

app = Flask(__name__)
CORS(app)


def error_json(message):
    return Response(
        json.dumps({"status": "error", "error": message}), mimetype="application/json"
    )


def success_json(data):
    if data:
        return Response(
            json.dumps({"status": "success", "data": data}), mimetype="application/json"
        )
    else:
        return Response(json.dumps({"status": "success"}), mimetype="application/json")


@app.route("/api", methods=["GET", "POST"])
def getData():
    try:
        if request.method == "POST":
            id = request.get_json(True)["identifier"]
        else:
            id = request.args.get("v")
    except:
        return error_json("No identifier specified"), 400
    if not id:
        return error_json("No identifier specified"), 400
    try:
        data = ytdl.extract_info(id, download=False)
        return success_json(data)
    except Exception as e:
        return error_json(str(e))


@app.route("/watch")
def watch():
    try:
        id = request.args.get("v")
    except:
        return error_json("No identifier specified"), 400
    if not id:
        return error_json("No identifier specified"), 400
    try:
        try:
            fmt = int(request.args.get("fmt"))
        except:
            fmt = None
        data = ytdl.extract_info(id, download=False)
        return redirect(data["formats"][fmt if fmt else -1]["url"], 302)
    except Exception as e:
        return error_json(str(e))


if __name__ == "__main__":
    app.run(debug=True, port=3000)
