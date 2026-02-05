import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')
import numpy as np
import csv

def visualize_data(file_path :str):
	f = open(file_path)
	reader = csv.reader(f)
	next(reader)
	data = []
	for row in reader:
		km = float(row[0])
		price = float(row[1])
		data.append((km, price))
	
	# Trier par kilométrage (x)
	data.sort(key=lambda pair: pair[0])
	
	# Séparer x et y après le tri
	x_values = [pair[0] for pair in data]
	y_values = [pair[1] for pair in data]
	
	plt.bar(x_values, y_values)
	plt.xticks(rotation=45)  
	plt.savefig('graph.png', dpi=150, bbox_inches='tight')
