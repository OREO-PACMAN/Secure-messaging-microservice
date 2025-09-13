from flask import Flask, request, jsonify
import sqlite3
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate encryption key (save this in real project!)
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    user = data["user"]
    message = data["message"].encode()

    encrypted = cipher.encrypt(message)

    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (user, encrypted))
    conn.commit()
    conn.close()

    return jsonify({"status": "Message stored securely"})

@app.route("/receive", methods=["GET"])
def receive():
    user = request.args.get("user")

    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("SELECT message FROM messages WHERE user=?", (user,))
    rows = c.fetchall()
    conn.close()

    decrypted = [cipher.decrypt(row[0]).decode() for row in rows]

    return jsonify({"messages": decrypted})

if __name__ == "__main__":
    app.run(ssl_context=("cert.pem", "key.pem"))
