import tkinter as tk
from tkinter import ttk
import heapq
import time

class DijkstraComparisonVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra's Algorithm Comparison")

        self.canvas_width = 600
        self.canvas_height = 400

        # Graph: adjacency list with weights
        self.graph = {
            'A': [('B', 2), ('C', 5)],
            'B': [('A', 2), ('C', 6), ('D', 1)],
            'C': [('A', 5), ('B', 6), ('E', 3)],
            'D': [('B', 1), ('E', 1), ('F', 4)],
            'E': [('C', 3), ('D', 1), ('G', 2)],
            'F': [('D', 4), ('G', 1)],
            'G': [('E', 2), ('F', 1)],
        }

        # Positions of nodes on canvas
        self.positions = {
            'A': (100, 100),
            'B': (200, 80),
            'C': (250, 150),
            'D': (300, 80),
            'E': (350, 170),
            'F': (400, 80),
            'G': (450, 150),
        }

        self.start_node = 'A'
        self.end_node = 'G'

        # Variables for both algorithms
        self.reset_state()

        # UI setup
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="nw")

        ttk.Label(self.frame, text="Dijkstra's Algorithm Comparison", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=5)

        ttk.Label(self.frame, text="Choose Algorithm:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.alg_var = tk.StringVar(value="heap")
        ttk.Radiobutton(self.frame, text="Min-Heap", variable=self.alg_var, value="heap").grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(self.frame, text="Linear Search", variable=self.alg_var, value="linear").grid(row=3, column=0, sticky="w")

        self.start_button = ttk.Button(self.frame, text="Start Algorithm", command=self.start_algorithm)
        self.start_button.grid(row=4, column=0, pady=10)

        self.step_button = ttk.Button(self.frame, text="Next Step", command=self.next_step, state="disabled")
        self.step_button.grid(row=5, column=0, pady=5)

        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=6, column=0, pady=5)

        self.status_label = ttk.Label(self.frame, text="Select algorithm and click Start.", font=("Arial", 12), wraplength=280)
        self.status_label.grid(row=7, column=0, pady=10)

        self.time_label = ttk.Label(self.frame, text="Elapsed time: 0.0 ms", font=("Arial", 12))
        self.time_label.grid(row=8, column=0, pady=5)

        self.winner_label = ttk.Label(self.frame, text="", font=("Arial", 14, "bold"), foreground="green")
        self.winner_label.grid(row=9, column=0, pady=10)

        # Canvas for graph visualization
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

        # Canvas for priority queue or linear search visualization
        self.queue_canvas = tk.Canvas(root, width=200, height=self.canvas_height, bg="#f0f0f0")
        self.queue_canvas.grid(row=0, column=2, padx=10, pady=10)

        self.draw_map()

    def reset_state(self):
        # Common state
        self.distances = {node: float('inf') for node in self.graph}
        self.distances[self.start_node] = 0
        self.prev = {node: None for node in self.graph}
        self.visited = set()

        # Heap-based
        self.pq = []

        # Linear search
        self.unvisited = set(self.graph.keys())

        # Timing
        self.start_time = None
        self.elapsed_time = 0.0

        # Step control
        self.algorithm_running = False
        self.finished = False

        # Current node being processed
        self.current_node = None

    def reset(self):
        self.reset_state()
        self.draw_map()
        self.queue_canvas.delete("all")
        self.status_label.config(text="Select algorithm and click Start.")
        self.time_label.config(text="Elapsed time: 0.0 ms")
        self.winner_label.config(text="")
        self.start_button.config(state="normal")
        self.step_button.config(state="disabled")

    def draw_map(self):
        self.canvas.delete("all")
        # Draw edges
        for node, neighbors in self.graph.items():
            x1, y1 = self.positions[node]
            for nbr, w in neighbors:
                x2, y2 = self.positions[nbr]
                self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                self.canvas.create_text(mid_x, mid_y - 10, text=str(w), font=("Arial", 10, "italic"))

        # Draw nodes
        radius = 20
        for node, (x, y) in self.positions.items():
            fill_color = "ligh