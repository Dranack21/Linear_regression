import sys
import os
from dotenv import load_dotenv

load_dotenv()
def predict(mileage: int) -> float:
    prediction :float
    t0 :float = float(os.getenv("t0"))
    t1 :float = float(os.getenv("t1"))
    prediction = t0 + mileage * t1
    return (prediction)
    

def main():
	print(sys.argv[1])
	predicted :float = predict(float(sys.argv[1]))
	print(predicted)
    


if __name__ == "__main__":
    main()