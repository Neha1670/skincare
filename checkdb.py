from flask import Flask, request

app = Flask(__name__)

with app.test_request_context(json={"product_id": 33, "quantity": 2}):
    print(request.get_json())  # Ye dikhaega kya data aa raha hai



