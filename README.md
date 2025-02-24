### Implementation of Naive Convex Hull Algorithm (Greedy) and Graham Scan Algorithm

Benchmark includes tests with input size n = 1000, 10 000, 100 000 points. Measures time elapsed.

Run with `python grahamScan.py`

Naive uses cross-product to check fitness of each consecutive possible point for convex hull. Graham Scan uses polar angle sort to determine order of consideration, and last-angle-concavity to pop unfit points.

Naive implementation should have worstcase runtime of $O(n^2)$ and Graham Scan should have runtimt of $O(n\log n)$.