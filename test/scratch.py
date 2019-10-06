import numpy as np
import time

seed_time = time.time()
print("SEED:", seed_time)

weights_to_use = [1,6,0,6,4,0,1,2,0,2,9,0,5,1,0,4,7]

probability = np.repeat(1 / len(weights_to_use), len(weights_to_use))
if np.count_nonzero(probability) > 0:
    max_value = np.max(weights_to_use)
    max_value_list = np.repeat(max_value, len(weights_to_use))

    weights_to_use - np.asarray(weights_to_use)

    numerator = max_value_list - weights_to_use
    print(numerator)

    probability = numerator / max_value_list
    print(probability)

candidates = np.argwhere(probability == np.amax(probability))
candidates = candidates.flatten().tolist()
print(candidates)

np.random.seed(int(seed_time))
choice = np.random.choice(candidates)

print(choice)