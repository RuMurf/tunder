from utils import *
import sys
sys.path.append('C:\\Users\\Ruairi\\Projects\\tunder\\application')


file = sys.argv[1]

result = match_from_file(file, "paramater_tuning", "test 1", footprint=10)

print(result)
sys.stdout.flush()