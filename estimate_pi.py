import random
from typing import List

import imageio
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt


def point_is_in_circle(x: float, y: float, radius: float) -> bool:
    if x ** 2 + y ** 2 <= radius ** 2:
        return True
    else:
        return False


def generate_random_point(lower_boud, upper_bound):
    return [random.uniform(lower_boud, upper_bound), random.uniform(lower_boud, upper_bound)]


def estimate_pi(random_points: List[List[float]], radius: float):
    in_circle = [point_is_in_circle(*point, radius) for point in random_points]
    return 4 * (1 / len(random_points)) * sum(in_circle)


def generate_points_and_estimate_pi(sample_size: int, radius):
    random_points = [generate_random_point(-radius, radius) for i in range(sample_size)]
    return estimate_pi(random_points, radius)


def continous_improvement_demo(sample_sizes: List[int], radius=1):
    # sample_sizes = [10, 100, 1000, 10000]
    initial_sample = [generate_random_point(-radius, radius) for i in range(sample_sizes[0])]
    points_in = list(filter(lambda point: point_is_in_circle(point[0], point[1], radius), initial_sample))
    points_out = list(filter(lambda point: point not in points_in, initial_sample))
    memory = {
        sample_sizes[0]: {
            "points": initial_sample,
            "estimate": estimate_pi(initial_sample, radius),
            "points_in": points_in,
            "points_out": points_out,
        }
    }
    for i in range(1, len(sample_sizes)):
        new_points = memory[sample_sizes[i - 1]]["points"]
        while len(new_points) < sample_sizes[i]:
            new_points.append(generate_random_point(-radius, radius))
        points_in = list(filter(lambda point: point_is_in_circle(point[0], point[1], radius), new_points))
        points_out = list(filter(lambda point: point not in points_in, new_points))
        memory[sample_sizes[i]] = {
            "points": new_points,
            "points_in": points_in,
            "points_out": points_out,
            "estimate": estimate_pi(new_points, radius)
        }
    return memory


def make_demo_graph(radius=1):
    sample_sizes = [i for i in range(1, 1000) if i % 20 == 0] + \
                   [i for i in range(1000, 5000) if i % 50 == 0] + \
                   [i for i in range(5000, 10000) if i % 100 == 0] + \
                   [10000] * 10
    demo_data = continous_improvement_demo(sample_sizes)
    image_paths = []
    for sample_size in sample_sizes:
        fig, ax = plt.subplots()
        ax.set_xlim(-radius, radius)
        ax.set_ylim(-radius, radius)
        circle1 = plt.Circle((0.0, 0.0), radius, color='lightgray')
        ax.add_artist(circle1)
        x_values_in = list(map(lambda tup: tup[0], demo_data[sample_size]["points_in"]))
        y_values_in = list(map(lambda tup: tup[1], demo_data[sample_size]["points_in"]))
        ax.scatter(x_values_in, y_values_in, facecolor="red", zorder=100, s=1)
        x_values_out = list(map(lambda tup: tup[0], demo_data[sample_size]["points_out"]))
        y_values_out = list(map(lambda tup: tup[1], demo_data[sample_size]["points_out"]))
        ax.scatter(x_values_out, y_values_out, facecolor="black", zorder=100, s=1)
        plt.title("Sample size = {sample_size}\n"
                  "Pi estimate = {pi}.".format(sample_size=sample_size, pi=round(demo_data[sample_size]["estimate"], 5)), loc='left')
        path = "/home/jjb/Dropbox/Programming/GIT/monte-carlo/graphs/graph_{sample_size}_{random}.png".format(sample_size=sample_size,
                                                                                                              random=random.randint(1, 10000))
        plt.savefig(path)
        image_paths.append(path)
        fig.clf()
        plt.clf()
        plt.close('all')
    images = []
    for filename in image_paths:
        images.append(imageio.imread(filename))
    imageio.mimsave("/home/jjb/Dropbox/Programming/GIT/monte-carlo/graphs/pi_estiamte_evolution.gif", images)


if __name__ == "__main__":
    # sample_size = int(sys.argv[1])
    # radius = int(sys.argv[2])
    # print(generate_points_and_estimate_pi(sample_size, radius))
    # mem = continous_improvement_demo([10, 100, 1000, 10000])
    make_demo_graph()


    # all_values = {}
    # error_made = {}
    # for i in range(8):
    #     sample_size = int(round(10 * 10 ** i, 0))
    #     range_size = int(round(10000000 * 10 ** (-i), 0))
    #     t0 = time.time()
    #     np.mean([estimate_pie(sample_size, 1) for i in range(range_size)])
    #     all_values[sample_size] = time.time() - t0
    #     print(sample_size*range_size)
