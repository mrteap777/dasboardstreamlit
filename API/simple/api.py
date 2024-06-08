from flask import Flask, jsonify, request #pip install flask

app = Flask(__name__)


users = [
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Jane", "email": "jane@example.com"},
]


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"})


@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    users.append(new_user)
    return jsonify(new_user)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.get_json()
    for i, user in enumerate(users):
        if user['id'] == user_id:
            users[i] = updated_user
            return jsonify(updated_user)
    return jsonify({"error": "User not found"})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for i, user in enumerate(users):
        if user['id'] == user_id:
            del users[i]
            return jsonify({"result": "User deleted"})
    return jsonify({"error": "User not found"})

if __name__ == '__main__':
    app.run(debug=True)