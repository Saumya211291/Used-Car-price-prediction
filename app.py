from flask import Flask, render_template, url_for, request, redirect
import pickle
import math
app = Flask(__name__)


predicted_score = None

@app.route('/')
def index():
	return render_template('index.html', score=predicted_score)

@app.route('/predict', methods=['GET', 'POST'])
def prediction():
	with open('models/model.pkl' , 'rb') as f:
		lr = pickle.load(f)
	global predicted_score
	if request.method == 'POST':
		req = request.form
		predict = [[]]
		present_price = float(req['present_price'])
		predict[0].append(present_price)
		kms_driven = int(req['kms_driven'])
		predict[0].append(kms_driven)
		owners = int(req['owners'])
		predict[0].append(owners)
		year_of_purchase = int(req['year_of_purchase'])
		year_of_purchase = 2022 - year_of_purchase
		predict[0].append(year_of_purchase)
		fuel_type = req['fuel_type']
		if fuel_type == "Petrol":
			predict[0].append(0)
			predict[0].append(1)
		if fuel_type == "Diesel":
			predict[0].append(1)
			predict[0].append(0)
		if fuel_type == "CNG":
			predict[0].append(0)
			predict[0].append(0)
		seller_type = int(req['seller_type'])
		predict[0].append(seller_type)
		tranmission_type = int(req['tranmission_type'])
		predict[0].append(tranmission_type)
		# predict.reshape(-1,1)
		predicted_price = lr.predict(predict)
		return render_template('predict.html', score=round(predicted_price[0],2))
		
	else:
		return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, port=8000)
