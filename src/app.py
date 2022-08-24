from flask import Flask, request, jsonify

app = Flask(__name__)

humans = []

#decoradores 
@app.route('/')
def hello_world():
    return '<h1>Welcome</h1>'


@app.route('/humans', methods=['GET'])
@app.route('/humans/<int:user_id>', methods=['GET'])
def handle_humans(user_id = None):
    if request.method == 'GET':
        if user_id is None:
            return humans , 200
        else:
            human = list(filter(lambda item: item["id"] == user_id, humans))
            return human, 200
    return humans, 405


@app.route('/humans', methods=['POST'])
def add_new_human():
    if request.method == 'POST':
        body = request.json
        if  body.get("name") is None:
            return {"message":"error propertie bad "} ,400
        if body.get("lastname") is None:
            return jsonify({"message":"error propertie bad "} ,400)
        
        body.update({"id": len(humans)+1})

        humans.append(body)
        return humans, 201


@app.route('/humans/<int:human_id>', methods=['PUT', 'DELETE'])#actualizar
def update_human(human_id=None):
    if request.method == 'PUT':
        body = request.json
        new_human = list(filter(lambda item: item["id"] == human_id, humans))
        if len(new_human) <=0:
            return jsonify({"message":"error not found"}), 404
        else:
            new_human = new_human[0]
            new_human["name"] = body["name"]
            new_human["lastname"] = body.get("lastname")

            print(new_human)
            return jsonify(new_human), 200
        
        print(body, human_id)
        return jsonify([]), 200


    if request.method == 'DELETE':
        if human_id is not None:
            for item in humans:
                if item["id"] == human_id:
                    humans.remove(item)
                    return jsonify([]), 204

            return jsonify({"message":"error not found"}), 404
        return jsonify({"message":"error not found"}), 404
    return jsonify([]), 405



if __name__=="__main__":
    app.run(host='0.0.0.0', port="8000", debug=True)
# app.run(host="0.0.0.0", debug=True)


