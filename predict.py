import sys
import csv
import os
from dotenv import load_dotenv
from visualize import visualize_data
from train  import get_min_max
load_dotenv()

def main() -> float:
	if len(sys.argv) != 1:
		print("Error: expecting zero arguments.")
		return(0.0)
	try:
		mileage = float(input("Enter a mileage: "))
	except ValueError:
		print("Error: Invalid mileage value. Please provide a number.")
		return(0.0)
	t0_str = os.getenv('theta0')
	t1_str = os.getenv('theta1')
	if (t0_str == None or t1_str == None):
		print("Error: Missing values inside env file.")
		return(0.0)
	try:
		t0 = float(t0_str)
		t1 = float(t1_str)
	except ValueError:
		print("Error: Invalid thetas values inside .env.")
		return(0.0)
	
	min_km, max_km, min_price, max_price = get_min_max() #Normalize
	normalized_mileage = (mileage - min_km) / (max_km - min_km)
	normalized_prediction = t0 + normalized_mileage * t1
	prediction = normalized_prediction * (max_price - min_price) + min_price #Denormalize
	if (prediction < 0):
		prediction = 0
	error = visualize_data("data.csv", min_km, max_km, max_price, min_price)
	print(f"Price with given mileage :{prediction}")
	print(f"Mean error: {error}%")
	return (prediction)


if __name__ == "__main__":
	main()