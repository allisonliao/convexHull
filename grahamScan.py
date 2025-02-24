# 02.24.25
# Allison Liao
# Computational Geometry, Assignment #3
# Implements both naive convex hull algorithm as well as Graham Scan 
# convex hull algorithm. Performs three test cases with visualizations 
# and takes a benchmark at 1000, 10000, 100000 input points to measure 
# the efficiency of each algorithm.

import random
import time
import matplotlib.pyplot as plt
from itertools import combinations
from math import atan2

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

# cross product function
def cross_product(p, q, r):
    return (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)

# naive convex hull algorithm
def naive_convex_hull(points):
    hull = set()
    
    for a, b in combinations(points, 2):  # iterate over all pairs of points
        # track if points are on both sides of line
        left = right = False  
        
        for p in points:
            if p == a or p == b:
                continue
            
            cp = cross_product(a, b, p)
            
            if cp > 0:
                left = True
            elif cp < 0:
                right = True
            
            if left and right:
                # if we have points on both sides, (a, b) is not in hull
                break
        
        if not (left and right):  
            # if all points are on one side, add both endpoints to hull
            hull.add(a)
            hull.add(b)
    
    # sort the list into ccw order
    hull = list(hull)

    # find the bottom-left (or leftmost) point (reference point)
    ref_point = min(hull, key=lambda p: (p.y, p.x))

    # Use polar angle to sort with respect to the reference point
    hull.sort(key=lambda p: (atan2(p.y - ref_point.y, p.x - ref_point.x), p.x))
    return hull

# graham scan algorithm
def graham_scan(points):
    points = sorted(points)
    
    def construct_half_hull(points):
        hull = []
        for p in points:
            while len(hull) >= 2 and cross_product(hull[-2], hull[-1], p) <= 0:
                hull.pop()
            hull.append(p)
        return hull
    
    lower_hull = construct_half_hull(points)
    upper_hull = construct_half_hull(reversed(points))
    
    # remove duplicates at endpoints
    return lower_hull[:-1] + upper_hull[:-1]  

# function to generate random point sets
def generate_points(n, low=-1000, high=1000, circular=False):
    if circular:
        return [Point(int(500 * random.cos(2 * 3.14159 * i / n)), int(500 * random.sin(2 * 3.14159 * i / n))) for i in range(n)]
    else:
        return [Point(random.randint(low, high), random.randint(low, high)) for _ in range(n)]

# function to plot hull
def plot_hull(points, hull, title):
    plt.figure()
    plt.scatter([p.x for p in points], [p.y for p in points], label='Points')
    hull.append(hull[0])  # close the hull
    plt.plot([p.x for p in hull], [p.y for p in hull], 'r-', label='Convex Hull')
    plt.legend()
    plt.title(title)
    pdftitle = title.replace(" ", "")
    pdftitle += ".pdf"
    plt.savefig(pdftitle, format='pdf')
    plt.show()

# benchmark function that times the algorithms and runs tests
def benchmark():
    sizes = [1000, 10000, 100000]
    for n in sizes:
        points = generate_points(n)
        
        start = time.time()
        naive_hull = naive_convex_hull(points)
        naive_time = time.time() - start
        
        start = time.time()
        graham_hull = graham_scan(points)
        graham_time = time.time() - start
        
        print(f"n={n}: Naive={naive_time:.4f}s, Graham={graham_time:.4f}s")

def main():
    # baseline test
    test_points = generate_points(20)
    naive_hull = naive_convex_hull(test_points)
    graham_hull = graham_scan(test_points)
    print("Naive Hull:", naive_hull)
    print("Graham Hull:", graham_hull)
    plot_hull(test_points, naive_hull, "Naive Convex Hull - 20 points")
    plot_hull(test_points, graham_hull, "Graham Scan Convex Hull - 20 points")

    # edge-case tests
    test_collinear = [Point(10, random.randint(0, 20)) for i in range(10)]
    graham_hull_collinear = graham_scan(test_collinear)
    plot_hull(test_collinear, graham_hull_collinear, "Graham Scan Edgecase - Collinear")

    test_zigzag = [Point(0,0), Point(1,5), Point(2,-5), Point(3,10), Point(4, -10), Point(5,12), Point(6, -12)]
    graham_hull_zigzag = graham_scan(test_zigzag)
    plot_hull(test_zigzag, graham_hull_zigzag, "Graham Scan Edgecase - Zigzag")

    test_grouped = [Point(random.randint(0,5), random.randint(0, 5)) for i in range(10)]
    test_grouped.append(Point(20, 20))
    graham_hull_grouped = graham_scan(test_grouped)
    plot_hull(test_grouped, graham_hull_grouped, "Graham Scan Edgecase - Grouped")

    # run benchmark
    benchmark()

    # RESULTS
    # n=1000: Naive=0.7192s, Graham=0.0013s
    # n=10000: Naive=69.1724s, Graham=0.0160s
    # n=100000: Naive=9046.7429s, Graham=0.1899s


    # TIME ANALYSIS
    # Although we expect the naive implementation to increase by a factor
    # of 10^3 when n increases by 10, the actual time increased by less than 
    # 10^2. This could be because of python's built in hash/set efficiencies.

    # For the Graham's Scan implementation, we expect that when n increases
    # by 10, the runtime would increase by 10 * log_2(10) or about 33x.
    # Similarly, this implementation performed a little better than expected.

if __name__ == "__main__":
    main()