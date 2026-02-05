from matplotlib import pyplot as plt
import csv
import os

def visualize_data(file_path :str, min_km : float, max_km :float, max_price : float, min_price) -> float:
	x_values = []
	y_values = []
	y_regression = []
	accuracy_list = []
	f = open(file_path)
	reader = csv.reader(f)
	next(reader)
	data = []
	for row in reader:
		km = float(row[0])
		price = float(row[1])
		data.append((km, price))
	
	data.sort(key=lambda pair: pair[0])	
	for pair in data:
		x_values.append(pair[0])
		y_values.append(pair[1])
	plt.plot(x_values, y_values)

	theta0 = float(os.getenv('theta0', 0))
	theta1 = float(os.getenv('theta1', 0))

	for mileage in x_values:
		normalized_mileage = (mileage - min_km) / (max_km - min_km)
		normalized_prediction = theta0 + theta1 * normalized_mileage
		x = normalized_prediction * (max_price - min_price) + min_price
		y_regression.append(x)
	
	for i in range (len(y_values)):
		real_price = y_values[i]
		predicted_price = y_regression[i]
		accuracy_list.append(abs(real_price - predicted_price) / real_price * 100)

	error = sum(accuracy_list)/len(accuracy_list)

	
	plt.plot(x_values ,y_regression, 'r')
	plt.xlabel('Kilométrage')
	plt.ylabel('Prix')
	plt.xticks(rotation=45)  
	plt.show()
	return (error)
