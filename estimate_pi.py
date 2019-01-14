import random

import sys


def point_is_in_circle(x: float, y: float, radius: float) -> bool:
    if x ** 2 + y ** 2 <= radius ** 2:
        return True
    else:
        return False


def generate_random_point(lower_boud, upper_bound):
    return [random.uniform(lower_boud, upper_bound), random.uniform(lower_boud, upper_bound)]


def estimate_pie(sample_size: int, radius):
    random_points = [generate_random_point(-radius, radius) for i in range(sample_size)]
    in_circle = [point_is_in_circle(*point, radius) for point in random_points]
    return 4 * (1 / sample_size) * sum(in_circle)


if __name__ == "__main__":
    sample_size = sys.argvs[1]
    radius = sys.argv[2]
