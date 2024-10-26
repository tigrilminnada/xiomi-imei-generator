import random
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

phone_models = [
    ("Poco M4", "860036062846822"),
    ("MI 14T PRO", "862998071243069"),
    ("MI 14T", "868329070436252"),
    ("MI 13T", "863660063000159"),
    ("MI 13T PRO", "869521065711736"),
    ("MI 14", "861482064823865"),
    ("NOTE 13", "860232060188446")
]

@app.route("/", methods=["GET", "POST"])
def index():
    imei_list = [] 
    if request.method == "POST":
        selected_model = request.form.get("model")
        quantity = int(request.form.get("quantity", 1))
        custom_imei = request.form.get("custom_imei")

        if selected_model and selected_model != "Select Model":
            try:
                # Case-insensitive comparison for model name
                imei_prefix = next((model[1] for model in phone_models if model[0].lower() == selected_model.lower()))  
                imei_list = generate_imei(imei_prefix, quantity)
            except StopIteration:
                print(f"Error: Model not found - {selected_model}") 
                return "Selected phone model not found."  # This should be displayed on the page
        elif custom_imei:
            imei_list = generate_custom_imei(custom_imei, quantity)

    return render_template("index.html", phone_models=phone_models, imei_list=imei_list)

def generate_imei(imei_prefix, quantity):
    imei_list = []
    for _ in range(quantity):
        random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))
        imei = imei_prefix[:-4] + random_digits
        imei_list.append(imei)
    return imei_list

def generate_custom_imei(imei, quantity):
    imei_list = []
    for _ in range(quantity):
        random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))
        new_imei = imei[:-4] + random_digits
        imei_list.append(new_imei)
    return imei_list

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)