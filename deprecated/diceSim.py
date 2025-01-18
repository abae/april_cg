import random
import matplotlib.pyplot as plt

def flip_coin():
    result = random.random()
    if result > .165203:
        return 'heads'
    else:
        return 'tails'

def simulate_coin_flips(num_flips):
    heads_count = 100
    heads_percentage = []

    for i in range(num_flips):
        if flip_coin() == 'heads':
            heads_count += 0.02
        else:
            heads_count -= 0.1

        heads_percentage.append(heads_count)

    return heads_percentage

num_flips = 1000000
heads_percentage = simulate_coin_flips(num_flips)

plt.plot(range(1, num_flips + 1), heads_percentage)
plt.axhline(y=0.5, color='r', linestyle='--')
plt.xlabel('Number of Flips')
plt.ylabel('Percentage of Heads')
plt.title('Coin Flip Probability Over Flips')
plt.show()