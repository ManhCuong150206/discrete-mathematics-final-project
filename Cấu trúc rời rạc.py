import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import math
from collections import deque
import heapq

# ================== CONSTANTS ==================
RADIUS = 20
COLORS = {
    'default': '#4A90E2',
    'selected': '#E74C3C',
    'visited': '#F39C12',
    'path': '#27AE60',
    'bipartite1': '#FF6B9D',
    'bipartite2': '#95E1D3',
    'mst': '#9B59B6',
    'current': '#E67E22'
}

# ================== MAIN CLASS ==================
class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualizer - Đồ Thị")
        self.root.geometry("1200x800")
        
        self.vertices = []
        self.edges = []
        self.weights = {}
        self.vertex_items = []
        self.edge_items = {}
        self.selected_vertex = None
        self.animation_speed = 500
        self.is_directed = False
        self.is_weighted = False
        
        self.setup_ui()
        
    def setup_ui(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Graph", command=self.clear_graph)
        file_menu.add_command(label="Save Graph", command=self.save_graph)
        file_menu.add_command(label="Load Graph", command=self.load_graph)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(main_container, width=250, bg='#f0f0f0')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        canvas_frame = tk.Frame(main_container)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        self.setup_controls(left_panel)
        
    def setup_controls(self, parent):
        settings_frame = tk.LabelFrame(parent, text="Cài Đặt Đồ Thị", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.directed_var = tk.BooleanVar()
        tk.Checkbutton(settings_frame, text="Có hướng", variable=self.directed_var, 
                      command=self.toggle_directed, bg='#f0f0f0').pack(anchor=tk.W, padx=5, pady=2)
        
        self.weighted_var = tk.BooleanVar()
        tk.Checkbutton(settings_frame, text="Có trọng số", variable=self.weighted_var,
                      command=self.toggle_weighted, bg='#f0f0f0').pack(anchor=tk.W, padx=5, pady=2)
        
        speed_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        speed_frame.pack(fill=tk.X, padx=5, pady=5)
        # tk.Label(speed_frame, text="Tốc độ:", bg='#f0f0f0').pack(side=tk.LEFT)
        # self.speed_scale = tk.Scale(speed_frame, from_=100, to=1000, orient=tk.HORIZONTAL,
        #                            command=self.update_speed, bg='#f0f0f0')
        # self.speed_scale.set(500)
        # self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        basic_frame = tk.LabelFrame(parent, text="Thao Tác Cơ Bản", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(basic_frame, text="Xóa đồ thị", command=self.clear_graph, bg='#E74C3C', fg='white').pack(fill=tk.X, padx=5, pady=2)
        tk.Button(basic_frame, text="Xóa đỉnh chọn", command=self.delete_selected, bg='#E67E22', fg='white').pack(fill=tk.X, padx=5, pady=2)
        
        path_frame = tk.LabelFrame(parent, text="Đường Đi Ngắn Nhất", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        path_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(path_frame, text="Tìm đường đi ngắn nhất ", command=self.run_shortest_path, 
                 bg='#27AE60', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        
        traversal_frame = tk.LabelFrame(parent, text="Duyệt Đồ Thị", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        traversal_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(traversal_frame, text="BFS (Duyệt theo chiều rộng)", command=self.run_bfs, 
                 bg='#3498DB', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        tk.Button(traversal_frame, text="DFS (Duyệt theo chiều sâu)", command=self.run_dfs, 
                 bg='#9B59B6', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        
        bipartite_frame = tk.LabelFrame(parent, text="Đồ Thị 2 Phía", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        bipartite_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(bipartite_frame, text="Kiểm tra đồ thị 2 phía", command=self.check_bipartite, 
                 bg='#E91E63', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        
        convert_frame = tk.LabelFrame(parent, text="Biểu Diễn Đồ Thị", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        convert_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(convert_frame, text="Ma trận kề", command=self.show_adj_matrix, 
                 bg='#607D8B', fg='white').pack(fill=tk.X, padx=5, pady=2)
        tk.Button(convert_frame, text="Danh sách kề", command=self.show_adj_list, 
                 bg='#546E7A', fg='white').pack(fill=tk.X, padx=5, pady=2)
        tk.Button(convert_frame, text="Danh sách cạnh", command=self.show_edge_list, 
                 bg='#455A64', fg='white').pack(fill=tk.X, padx=5, pady=2)
        
        advanced_frame = tk.LabelFrame(parent, text="Thuật Toán Nâng Cao", bg='#f0f0f0', font=('Arial', 10, 'bold'))
        advanced_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(advanced_frame, text="7.1 Prim (Cây khung)", command=self.run_prim, 
                 bg='#8E44AD', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        tk.Button(advanced_frame, text="7.2 Kruskal (Cây khung)", command=self.run_kruskal, 
                 bg='#9B59B6', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        tk.Button(advanced_frame, text="7.3 Ford-Fulkerson (Luồng)", command=self.run_ford_fulkerson, 
                 bg='#C0392B', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        tk.Button(advanced_frame, text="7.4 Fleury (Kiểm tra Euler)", command=self.check_euler, 
                 bg='#FF5722', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        tk.Button(advanced_frame, text="7.5 Hierholzer (Chu trình Euler)", command=self.run_hierholzer, 
                 bg='#D35400', fg='white', wraplength=200).pack(fill=tk.X, padx=5, pady=2)
        
    def clear_graph(self):
        self.vertices = []
        self.edges = []
        self.weights = {}
        self.vertex_items = []
        self.edge_items = {}
        self.selected_vertex = None
        self.canvas.delete("all")
        
    def toggle_directed(self):
        self.is_directed = self.directed_var.get()
        self.redraw_graph()
        
    def toggle_weighted(self):
        self.is_weighted = self.weighted_var.get()
        self.redraw_graph()
        
    def update_speed(self, val):
        self.animation_speed = int(val)
        
    def find_vertex(self, x, y):
        for i, (vx, vy) in enumerate(self.vertices):
            if math.hypot(vx - x, vy - y) <= RADIUS:
                return i
        return None
        
    def on_click(self, event):
        v = self.find_vertex(event.x, event.y)
        
        if v is None:
            self.vertices.append((event.x, event.y))
            self.draw_vertex(event.x, event.y, len(self.vertices) - 1)
        else:
            if self.selected_vertex is None:
                self.selected_vertex = v
                self.highlight_vertex(v, COLORS['selected'])
            else:
                if self.selected_vertex != v:
                    edge = (self.selected_vertex, v)
                    if edge not in self.edges and (not self.is_directed or (v, self.selected_vertex) not in self.edges):
                        self.edges.append(edge)
                        
                        if self.is_weighted:
                            weight = simpledialog.askinteger("Trọng số cạnh", "Nhập trọng số:", initialvalue=1)
                            if weight is None:
                                weight = 1
                            self.weights[edge] = weight
                        
                        self.draw_edge(self.selected_vertex, v)
                
                self.highlight_vertex(self.selected_vertex, COLORS['default'])
                self.selected_vertex = None
                
    def on_right_click(self, event):
        v = self.find_vertex(event.x, event.y)
        if v is not None:
            self.selected_vertex = v
            self.highlight_vertex(v, COLORS['selected'])
            
    def delete_selected(self):
        if self.selected_vertex is not None:
            v = self.selected_vertex
            self.vertices.pop(v)
            self.edges = [(u if u < v else u-1, w if w < v else w-1) 
                         for u, w in self.edges if u != v and w != v]
            
            new_weights = {}
            for (u, w), weight in self.weights.items():
                if u != v and w != v:
                    new_u = u if u < v else u-1
                    new_w = w if w < v else w-1
                    new_weights[(new_u, new_w)] = weight
            self.weights = new_weights
            
            self.selected_vertex = None
            self.redraw_graph()
            
    def draw_vertex(self, x, y, idx, color=None):
        if color is None:
            color = COLORS['default']
        oval = self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS,
                                      fill=color, outline='#2C3E50', width=2)
        text = self.canvas.create_text(x, y, text=str(idx), font=('Arial', 12, 'bold'), fill='white')
        self.vertex_items.append((oval, text))
        
    def draw_edge(self, u, v, color='#34495E', width=2):
        x1, y1 = self.vertices[u]
        x2, y2 = self.vertices[v]
        
        if self.is_directed:
            angle = math.atan2(y2 - y1, x2 - x1)
            x2_adj = x2 - RADIUS * math.cos(angle)
            y2_adj = y2 - RADIUS * math.sin(angle)
            line = self.canvas.create_line(x1, y1, x2_adj, y2_adj, width=width, fill=color, arrow=tk.LAST)
        else:
            line = self.canvas.create_line(x1, y1, x2, y2, width=width, fill=color)
        
        self.edge_items[(u, v)] = [line]
        
        if self.is_weighted and (u, v) in self.weights:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            weight_text = self.canvas.create_text(mx, my, text=str(self.weights[(u, v)]),
                                                 font=('Arial', 10, 'bold'), fill='#E74C3C', bg='white')
            self.edge_items[(u, v)].append(weight_text)
            
    def highlight_vertex(self, idx, color):
        if idx < len(self.vertex_items):
            oval, _ = self.vertex_items[idx]
            self.canvas.itemconfig(oval, fill=color)
            
    def highlight_edge(self, u, v, color, width=3):
        if (u, v) in self.edge_items:
            for item in self.edge_items[(u, v)]:
                if self.canvas.type(item) == 'line':
                    self.canvas.itemconfig(item, fill=color, width=width)
        elif not self.is_directed and (v, u) in self.edge_items:
            for item in self.edge_items[(v, u)]:
                if self.canvas.type(item) == 'line':
                    self.canvas.itemconfig(item, fill=color, width=width)
                    
    def reset_colors(self):
        for i in range(len(self.vertices)):
            self.highlight_vertex(i, COLORS['default'])
        for edge in self.edge_items:
            self.highlight_edge(edge[0], edge[1], '#34495E', 2)
            
    def redraw_graph(self):
        self.canvas.delete("all")
        self.vertex_items = []
        self.edge_items = {}
        
        for u, v in self.edges:
            self.draw_edge(u, v)
        for i, (x, y) in enumerate(self.vertices):
            self.draw_vertex(x, y, i)
            
    def build_adj_list(self):
        adj = {i: [] for i in range(len(self.vertices))}
        for u, v in self.edges:
            adj[u].append(v)
            if not self.is_directed:
                adj[v].append(u)
        return adj
    
    # ================== CÂU 3: SHORTEST PATH ==================
    def run_shortest_path(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
            
        start = simpledialog.askinteger("Đường đi ngắn nhất", "Nhập đỉnh bắt đầu:", initialvalue=0)
        end = simpledialog.askinteger("Đường đi ngắn nhất", "Nhập đỉnh kết thúc:", initialvalue=len(self.vertices)-1)
        
        if start is None or end is None or start >= len(self.vertices) or end >= len(self.vertices):
            return
            
        adj = self.build_adj_list()
        dist = [float("inf")] * len(self.vertices)
        prev = [None] * len(self.vertices)
        dist[start] = 0
        q = deque([start])
        
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == float("inf"):
                    dist[v] = dist[u] + 1
                    prev[v] = u
                    q.append(v)
                    
        if dist[end] == float("inf"):
            messagebox.showinfo("Kết quả", "Không có đường đi!")
            return
            
        self.reset_colors()
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        
        for i in range(len(path)):
            self.highlight_vertex(path[i], COLORS['path'])
            if i > 0:
                self.highlight_edge(path[i-1], path[i], COLORS['path'], 4)
            self.root.update()
            self.root.after(self.animation_speed)
            
        messagebox.showinfo("Kết quả", f"Độ dài: {dist[end]}\nĐường đi: {' → '.join(map(str, path))}")
    
    # ================== CÂU 4: TRAVERSAL ==================
    def run_bfs(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
            
        start = simpledialog.askinteger("BFS", "Nhập đỉnh bắt đầu:", initialvalue=0)
        if start is None or start >= len(self.vertices):
            return
            
        self.reset_colors()
        adj = self.build_adj_list()
        visited = [False] * len(self.vertices)
        q = deque([start])
        visited[start] = True
        order = []
        
        while q:
            u = q.popleft()
            order.append(u)
            self.highlight_vertex(u, COLORS['visited'])
            self.root.update()
            self.root.after(self.animation_speed)
            
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
                    self.highlight_edge(u, v, COLORS['path'])
        
        messagebox.showinfo("BFS", f"Thứ tự duyệt: {' → '.join(map(str, order))}")
    
    def run_dfs(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
            
        start = simpledialog.askinteger("DFS", "Nhập đỉnh bắt đầu:", initialvalue=0)
        if start is None or start >= len(self.vertices):
            return
            
        self.reset_colors()
        adj = self.build_adj_list()
        visited = [False] * len(self.vertices)
        order = []
        
        def dfs_visit(u):
            visited[u] = True
            order.append(u)
            self.highlight_vertex(u, COLORS['visited'])
            self.root.update()
            self.root.after(self.animation_speed)
            
            for v in adj[u]:
                if not visited[v]:
                    self.highlight_edge(u, v, COLORS['path'])
                    dfs_visit(v)
                    
        dfs_visit(start)
        messagebox.showinfo("DFS", f"Thứ tự duyệt: {' → '.join(map(str, order))}")
    
    # ================== CÂU 5: BIPARTITE ==================
    def check_bipartite(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
            
        adj = self.build_adj_list()
        color = [-1] * len(self.vertices)
        
        for start in range(len(self.vertices)):
            if color[start] == -1:
                q = deque([start])
                color[start] = 0
                
                while q:
                    u = q.popleft()
                    for v in adj[u]:
                        if color[v] == -1:
                            color[v] = 1 - color[u]
                            q.append(v)
                        elif color[v] == color[u]:
                            messagebox.showinfo("Kết quả", "Đồ thị KHÔNG phải đồ thị 2 phía!")
                            return
                            
        for i in range(len(self.vertices)):
            self.highlight_vertex(i, COLORS['bipartite1'] if color[i] == 0 else COLORS['bipartite2'])
            
        messagebox.showinfo("Kết quả", "Đồ thị LÀ đồ thị 2 phía!")
    
    # ================== CÂU 6: REPRESENTATIONS ==================
    def show_adj_matrix(self):
        n = len(self.vertices)
        if n == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
            
        matrix = [[0] * n for _ in range(n)]
        
        for u, v in self.edges:
            weight = self.weights.get((u, v), 1)
            matrix[u][v] = weight
            if not self.is_directed:
                matrix[v][u] = weight
                
        result = "MA TRẬN KỀ:\n\n"
        result += "   " + " ".join(f"{i:3}" for i in range(n)) + "\n"
        for i in range(n):
            result += f"{i:2} " + " ".join(f"{matrix[i][j]:3}" for j in range(n)) + "\n"
            
        self.show_text_window("Ma Trận Kề", result)
        
    def show_adj_list(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
            
        adj = self.build_adj_list()
        result = "DANH SÁCH KỀ:\n\n"
        
        for u in range(len(self.vertices)):
            result += f"Đỉnh {u}: "
            neighbors = []
            for v in adj[u]:
                if self.is_weighted:
                    weight = self.weights.get((u, v), self.weights.get((v, u), 1))
                    neighbors.append(f"{v}(w={weight})")
                else:
                    neighbors.append(str(v))
            result += " → ".join(neighbors) if neighbors else "∅"
            result += "\n"
            
        self.show_text_window("Danh Sách Kề", result)
        
    def show_edge_list(self):
        if not self.edges:
            messagebox.showwarning("Cảnh báo", "Không có cạnh!")
            return
            
        result = "DANH SÁCH CẠNH:\n\n"
        
        for i, (u, v) in enumerate(self.edges):
            if self.is_weighted:
                weight = self.weights.get((u, v), 1)
                result += f"Cạnh {i+1}: ({u}, {v}) - Trọng số: {weight}\n"
            else:
                result += f"Cạnh {i+1}: ({u}, {v})\n"
                
        self.show_text_window("Danh Sách Cạnh", result)
    
    # ================== CÂU 7.1: PRIM ==================
    def run_prim(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        if self.is_directed:
            messagebox.showwarning("Cảnh báo", "Prim chỉ áp dụng cho đồ thị vô hướng!")
            return
            
        self.reset_colors()
        adj = self.build_adj_list()
        in_mst = [False] * len(self.vertices)
        pq = [(0, 0, -1)]
        total_weight = 0
        edges_in_mst = []
        
        while pq:
            weight, u, parent = heapq.heappop(pq)
            
            if in_mst[u]:
                continue
                
            in_mst[u] = True
            total_weight += weight
            
            if parent != -1:
                edges_in_mst.append((parent, u, weight))
            
            self.highlight_vertex(u, COLORS['mst'])
            if parent != -1:
                self.highlight_edge(parent, u, COLORS['mst'], 4)
                
            self.root.update()
            self.root.after(self.animation_speed)
            
            for v in adj[u]:
                if not in_mst[v]:
                    edge_weight = self.weights.get((u, v), self.weights.get((v, u), 1))
                    heapq.heappush(pq, (edge_weight, v, u))
        
        result = f"Prim - Cây Khung Nhỏ Nhất\n\nTổng trọng số: {total_weight}\n\nCác cạnh:\n"
        for u, v, w in edges_in_mst:
            result += f"({u}, {v}) - w={w}\n"
            
        messagebox.showinfo("Prim", result)
    
    # ================== CÂU 7.2: KRUSKAL ==================
    def run_kruskal(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        if self.is_directed:
            messagebox.showwarning("Cảnh báo", "Kruskal chỉ áp dụng cho đồ thị vô hướng!")
            return
            
        self.reset_colors()
        
        parent = list(range(len(self.vertices)))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
            
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
                return True
            return False
            
        edge_list = []
        for u, v in self.edges:
            weight = self.weights.get((u, v), 1)
            edge_list.append((weight, u, v))
        edge_list.sort()
        
        total_weight = 0
        edges_in_mst = []
        
        for weight, u, v in edge_list:
            if union(u, v):
                total_weight += weight
                edges_in_mst.append((u, v, weight))
                self.highlight_edge(u, v, COLORS['mst'], 4)
                self.highlight_vertex(u, COLORS['mst'])
                self.highlight_vertex(v, COLORS['mst'])
                self.root.update()
                self.root.after(self.animation_speed)
        
        result = f"Kruskal - Cây Khung Nhỏ Nhất\n\nTổng trọng số: {total_weight}\n\nCác cạnh:\n"
        for u, v, w in edges_in_mst:
            result += f"({u}, {v}) - w={w}\n"
                
        messagebox.showinfo("Kruskal", result)
    
    # ================== CÂU 7.3: FORD-FULKERSON ==================
    def run_ford_fulkerson(self):
            if not self.vertices or not self.is_weighted:
                messagebox.showwarning("Cảnh báo", "Đồ thị phải có trọng số!")
                return

            if not self.is_directed:
                messagebox.showwarning("Cảnh báo", "Max Flow cần đồ thị có hướng!")
                return

            source = simpledialog.askinteger("Max Flow", "Nhập đỉnh nguồn:", initialvalue=0)
            sink = simpledialog.askinteger(
                "Max Flow", 
                "Nhập đỉnh đích:", 
                initialvalue=len(self.vertices) - 1
            )

            if (
                source is None or sink is None or
                source < 0 or sink < 0 or
                source >= len(self.vertices) or
                sink >= len(self.vertices) or
                source == sink
            ):
                messagebox.showerror("Lỗi", "Đỉnh nguồn hoặc đích không hợp lệ!")
                return
        
            self.reset_colors()
        
            n = len(self.vertices)
            capacity = [[0] * n for _ in range(n)]
        
            for u, v in self.edges:
                capacity[u][v] = self.weights.get((u, v), 1)
        
            def bfs_find_path(s, t, parent):
                visited = [False] * n
                q = deque([s])
                visited[s] = True
        
                while q:
                    u = q.popleft()
                    for v in range(n):
                        if not visited[v] and capacity[u][v] > 0:
                            visited[v] = True
                            parent[v] = u
                            if v == t:
                                return True
                            q.append(v)
                return False
        
            parent = [-1] * n
            max_flow = 0
        
            while bfs_find_path(source, sink, parent):
                path_flow = float('inf')
                v = sink
                path = []

                while v != source:
                    path.append(v)
                    u = parent[v]
                    path_flow = min(path_flow, capacity[u][v])
                    v = u
                path.append(source)
                path.reverse()

                v = sink
                while v != source:
                    u = parent[v]
                    capacity[u][v] -= path_flow
                    capacity[v][u] += path_flow
                    v = u

                max_flow += path_flow

                # Trực quan hóa đường tăng luồng
                for i in range(len(path)):
                    self.highlight_vertex(path[i], COLORS['current'])
                    if i > 0:
                        self.highlight_edge(path[i-1], path[i], COLORS['path'], 4)

                self.root.update()
                self.root.after(self.animation_speed)

                parent = [-1] * n

                messagebox.showinfo(
                "Ford-Fulkerson",
                f"Luồng cực đại từ {source} đến {sink}: {max_flow}"
                )
        

    
    # ================== CÂU 7.4: FLEURY (KIỂM TRA EULER) ==================
    def check_euler(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        adj = self.build_adj_list()
        
        if self.is_directed:
            in_degree = [0] * len(self.vertices)
            out_degree = [0] * len(self.vertices)
            
            for u, v in self.edges:
                out_degree[u] += 1
                in_degree[v] += 1
            
            start_vertices = sum(1 for i in range(len(self.vertices)) if out_degree[i] - in_degree[i] == 1)
            end_vertices = sum(1 for i in range(len(self.vertices)) if in_degree[i] - out_degree[i] == 1)
            balanced = sum(1 for i in range(len(self.vertices)) if in_degree[i] == out_degree[i])
            
            if start_vertices == 1 and end_vertices == 1 and balanced == len(self.vertices) - 2:
                messagebox.showinfo("Fleury", "Đồ thị có ĐƯỜNG ĐI EULER!")
            elif start_vertices == 0 and end_vertices == 0:
                messagebox.showinfo("Fleury", "Đồ thị có CHU TRÌNH EULER!")
            else:
                messagebox.showinfo("Fleury", "Đồ thị KHÔNG có đường đi hoặc chu trình Euler!")
        else:
            degrees = [len(adj[i]) for i in range(len(self.vertices))]
            odd_vertices = sum(1 for d in degrees if d % 2 == 1)
            
            if odd_vertices == 0:
                messagebox.showinfo("Fleury", "Đồ thị có CHU TRÌNH EULER!")
            elif odd_vertices == 2:
                messagebox.showinfo("Fleury", "Đồ thị có ĐƯỜNG ĐI EULER!")
            else:
                messagebox.showinfo("Fleury", "Đồ thị KHÔNG có đường đi hoặc chu trình Euler!")
    
    # ================== CÂU 7.5: HIERHOLZER ==================
    def run_hierholzer(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        adj = self.build_adj_list()
        
        if self.is_directed:
            in_degree = [0] * len(self.vertices)
            out_degree = [0] * len(self.vertices)
            
            for u, v in self.edges:
                out_degree[u] += 1
                in_degree[v] += 1
            
            start_vertices = [i for i in range(len(self.vertices)) if out_degree[i] - in_degree[i] == 1]
            end_vertices = [i for i in range(len(self.vertices)) if in_degree[i] - out_degree[i] == 1]
            balanced = [i for i in range(len(self.vertices)) if in_degree[i] == out_degree[i]]
            
            if len(start_vertices) == 1 and len(end_vertices) == 1 and len(balanced) == len(self.vertices) - 2:
                start = start_vertices[0]
                is_circuit = False
            elif len(start_vertices) == 0 and len(end_vertices) == 0:
                start = 0
                is_circuit = True
            else:
                messagebox.showinfo("Hierholzer", "Đồ thị KHÔNG có đường đi hoặc chu trình Euler!")
                return
        else:
            degrees = [len(adj[i]) for i in range(len(self.vertices))]
            odd_vertices = [i for i in range(len(self.vertices)) if degrees[i] % 2 == 1]
            
            if len(odd_vertices) == 0:
                start = 0
                is_circuit = True
            elif len(odd_vertices) == 2:
                start = odd_vertices[0]
                is_circuit = False
            else:
                messagebox.showinfo("Hierholzer", "Đồ thị KHÔNG có đường đi hoặc chu trình Euler!")
                return
        
        # Thuật toán Hierholzer
        adj_copy = {i: adj[i][:] for i in range(len(self.vertices))}
        stack = [start]
        path = []
        
        while stack:
            u = stack[-1]
            if adj_copy[u]:
                v = adj_copy[u].pop()
                if not self.is_directed:
                    adj_copy[v].remove(u)
                stack.append(v)
            else:
                path.append(stack.pop())
        
        path.reverse()
        
        if len(path) != len(self.edges) + 1:
            messagebox.showinfo("Hierholzer", "Đồ thị không liên thông! Không tìm được đường đi Euler.")
            return
        
        # Trực quan hóa
        self.reset_colors()
        
        for i in range(len(path)):
            self.highlight_vertex(path[i], COLORS['visited'])
            if i > 0:
                self.highlight_edge(path[i-1], path[i], COLORS['path'], 4)
                self.root.update()
                self.root.after(self.animation_speed)
        
        path_str = " → ".join(map(str, path))
        result_type = "Chu trình Euler" if is_circuit else "Đường đi Euler"
        messagebox.showinfo("Hierholzer", 
                           f"Tìm thấy {result_type}!\n\nĐường đi: {path_str}\n\nTổng số cạnh: {len(path)-1}")
    
    # ================== HELPER FUNCTIONS ==================
    def show_text_window(self, title, text):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("600x500")
        
        text_widget = tk.Text(window, wrap=tk.WORD, font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, text)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = tk.Scrollbar(text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
    
    # ================== FILE OPERATIONS (CÂU 2: LƯU ĐỒ THỊ) ==================
    def save_graph(self):
        if not self.vertices:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        data = {
            "vertices": self.vertices,
            "edges": self.edges,
            "weights": {f"{u},{v}": w for (u, v), w in self.weights.items()},
            "is_directed": self.is_directed,
            "is_weighted": self.is_weighted
        }
        
        file = filedialog.asksaveasfilename(
            defaultextension=".json", 
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file:
            try:
                with open(file, "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Thành công", "Đồ thị đã được lưu!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
            
    def load_graph(self):
        file = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file:
            return
        
        try:
            with open(file, "r", encoding='utf-8') as f:
                data = json.load(f)
            
            self.vertices = data["vertices"]
            self.edges = data["edges"]
            self.weights = {tuple(map(int, k.split(','))): v for k, v in data.get("weights", {}).items()}
            self.is_directed = data.get("is_directed", False)
            self.is_weighted = data.get("is_weighted", False)
            
            self.directed_var.set(self.is_directed)
            self.weighted_var.set(self.is_weighted)
            
            self.redraw_graph()
            messagebox.showinfo("Thành công", "Đồ thị đã được tải!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file: {str(e)}")

    def on_drag(self, event):
        if self.selected_vertex is not None:
            self.vertices[self.selected_vertex] = (event.x, event.y)
            self.redraw_graph()
# ================== MAIN ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()