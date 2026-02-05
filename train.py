import csv
import os
from dotenv import load_dotenv
from dotenv import set_key

load_dotenv()

def main():
	try:
		set_key('.env', 'theta0', '0')
		set_key('.env', 'theta1', '0')
	except PermissionError:
		print("Error: Permission denied to write to .env file")
		return None
	load_dotenv(override=True)
	print(float(os.getenv('theta0')))
	print(float(os.getenv('theta1')))

	try:
		min_km, max_km, min_price, max_price = get_min_max()
		normalized_list = normalize_data(min_km, max_km, min_price, max_price)
		lr : float  = find_best_lr(normalized_list)
		final_gradiant_descent(normalized_list, lr, float(os.getenv('theta0')) , float(os.getenv('theta1')))
	except FileNotFoundError:
		print("Error: data.csv file not found")
		return
	except PermissionError:
		print("Error: Permission denied to read data.csv")
		return
	except ValueError:
		print("Error: Invalid data format in CSV file")
		return
	except StopIteration:
		print("Error: CSV file is empty or missing data")
		return
	except IndexError:
		print("Error: CSV file has insufficient data")
		return

	
#Min max for normalize function
def get_min_max() -> float:
	f = open("data.csv")
	reader = csv.reader(f)
	next(reader)
	first_row = next(reader)
	min_km = max_km = float(first_row[0])
	min_price = max_price = float(first_row[1])
	for row in reader:
		km = float(row[0])
		price = float(row[1])
		if km < min_km:
			min_km = km
		if km > max_km:
			max_km = km
		if price < min_price:
			min_price = price
		if price > max_price:
			max_price = price

	f.close()
	return min_km, max_km, min_price, max_price


def normalize_data(min_km :float, max_km :float, min_price :float, max_price :float) -> list:
	tmp_km : float
	tmp_price: float
	normalized_list = []
	f = open("data.csv")
	reader = csv.reader(f)
	next(reader)
	for row in reader:
		tmp_km = (float(row[0]) - min_km)/ (max_km - min_km)
		tmp_price = (float(row[1]) - min_price) / (max_price - min_price)
		normalized_list.append((tmp_km, tmp_price))
	print(normalized_list)
	f.close()
	return (normalized_list)


###small gradiant descned with multiples LR to find the best one
def find_best_lr(normalized_list :list):
	best_lr = None
	best_mse = float('inf')
	lr_candidats = [0.001, 0.01, 0.1, 0.5, 1.0]
	
	for lr in lr_candidats:
		theta0 : float = 0
		theta1 : float = 0
		for i in range(200):
			tmp_theta0, tmp_theta1 = calculate_gradient(normalized_list, lr, theta0, theta1)
			# on ajuste les thetas avec les distances de "pas" qu'on a trouve
			theta0 = theta0 - tmp_theta0 
			theta1 = theta1 - tmp_theta1
			mse = calculate_mse(normalized_list, theta0, theta1)
		if mse < best_mse:
			best_mse = mse
			best_lr = lr
	return best_lr

def calculate_gradient(normalized_list : list, lr :float, theta0 :float, theta1 :float) -> float:
	m = len(normalized_list)
	sum_theta0 = 0
	sum_theta1 = 0

	for data in normalized_list:
		km = data[0]
		price = data[1]

		# estimation du prix avec notre thetas actuels
		estimated_price :float = theta0 + (theta1 * km)
		# Calcul de l'erreur (difference avec estimated - prix)
		error :float = estimated_price - price
		# 99->103 = Formules de tmp0 tmp1 du sujet
		sum_theta0 += error
		sum_theta1 += error * km

	theta0 = lr * (sum_theta0 / m)
	theta1 = lr * (sum_theta1 / m)
	return (theta0, theta1)

# MSE = measures how bad our model is, function to get tetas are derivated from it
# 1/m(sum of 1 ->m(Yi - Yî)²)
#m1∑( y^​−y)
def calculate_mse(normalized_list :list, theta0 :float, theta1 :float) -> float:
    m = len(normalized_list)
    total = 0
    
    for km, price in normalized_list:
        estimate = theta0 + theta1 * km  # ŷ
        error = estimate - price          # (ŷ - y)
        total += error ** 2               # (ŷ - y)²
    
    mse = total / m                       # 1/m
    return mse

def final_gradiant_descent(normalized_list :list, lr : float ,theta0 : float, theta1 :float):
	previous_mse = float('inf')
	max_iterations : int  = 10000
	for i in range (max_iterations):
		tmp_theta0, tmp_theta1 = calculate_gradient(normalized_list, lr, theta0, theta1)
		theta0 = theta0 - tmp_theta0 
		theta1 = theta1 - tmp_theta1
		current_mse = calculate_mse (normalized_list, theta0, theta1) #lower is better duh
		if abs(previous_mse - current_mse) < 0.000001 :
			print(f"Convergence atteinte à l'itération {i}")
			break
		previous_mse = current_mse
	set_key('.env', 'theta0', str(theta0))
	set_key('.env', 'theta1', str(theta1))
	return (theta0, theta1)
	

if __name__ == "__main__":
	main()