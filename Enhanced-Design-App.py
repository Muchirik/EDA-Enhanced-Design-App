import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk

class DesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Design App")
        self.root.geometry("900x700")

        # Default settings
        self.brush_color = "black"
        self.brush_size = 5
        self.eraser_mode = False
        self.drawing_tool = "free"  # Options: free, rectangle, circle, line, text
        self.start_x = None
        self.start_y = None
        self.undo_stack = []
        self.redo_stack = []
        self.grid_visible = False
        self.brush_style = "solid"  # Options: solid, dashed, dotted

        # Canvas setup
        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=10)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Toolbar
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(fill=tk.X)

        # Brush size slider
        tk.Label(self.toolbar, text="Brush Size:").pack(side=tk.LEFT, padx=5)
        self.size_slider = tk.Scale(self.toolbar, from_=1, to=20, orient=tk.HORIZONTAL)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.LEFT)

        # Color chooser button
        self.color_button = tk.Button(self.toolbar, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5)

        # Eraser button
        self.eraser_button = tk.Button(self.toolbar, text="Eraser", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT, padx=5)

        # Shape selection
        tk.Label(self.toolbar, text="Shapes:").pack(side=tk.LEFT, padx=5)
        self.shape_var = tk.StringVar(value="free")
        shapes = ["free", "rectangle", "circle", "line", "text"]
        for shape in shapes:
            tk.Radiobutton(self.toolbar, text=shape.capitalize(), variable=self.shape_var, value=shape,
                           command=self.select_shape).pack(side=tk.LEFT)

        # Brush style selection
        tk.Label(self.toolbar, text="Brush Style:").pack(side=tk.LEFT, padx=5)
        self.brush_style_var = tk.StringVar(value="solid")
        styles = ["solid", "dashed", "dotted"]
        for style in styles:
            tk.Radiobutton(self.toolbar, text=style.capitalize(), variable=self.brush_style_var, value=style,
                           command=self.select_brush_style).pack(side=tk.LEFT)

        # Undo/Redo buttons
        self.undo_button = tk.Button(self.toolbar, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5)
        self.redo_button = tk.Button(self.toolbar, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        # Save button
        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_canvas)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Grid toggle button
        self.grid_button = tk.Button(self.toolbar, text="Toggle Grid", command=self.toggle_grid)
        self.grid_button.pack(side=tk.LEFT, padx=5)

        # Gradient background button
        self.gradient_button = tk.Button(self.toolbar, text="Gradient Background", command=self.gradient_background)
        self.gradient_button.pack(side=tk.LEFT, padx=5)

        # Custom canvas size button
        self.resize_button = tk.Button(self.toolbar, text="Resize Canvas", command=self.resize_canvas)
        self.resize_button.pack(side=tk.LEFT, padx=5)

        # Clear button
        self.clear_button = tk.Button(self.toolbar, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Setup for saving the canvas
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def paint(self, event):
        """Draw freehand on the canvas."""
        if self.drawing_tool == "free":
            x1, y1 = event.x - self.brush_size, event.y - self.brush_size
            x2, y2 = event.x + self.brush_size, event.y + self.brush_size
            color = "white" if self.eraser_mode else self.brush_color
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
            self.draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)

    def start_draw(self, event):
        """Start drawing shapes."""
        self.start_x, self.start_y = event.x, event.y

    def stop_draw(self, event):
        """Stop drawing shapes and finalize them."""
        if self.drawing_tool in ["rectangle", "circle", "line", "text"]:
            end_x, end_y = event.x, event.y
            color = "white" if self.eraser_mode else self.brush_color

            if self.drawing_tool == "rectangle":
                self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, outline=color, width=self.brush_size)
                self.draw.rectangle([self.start_x, self.start_y, end_x, end_y], outline=color, width=self.brush_size)
            elif self.drawing_tool == "circle":
                self.canvas.create_oval(self.start_x, self.start_y, end_x, end_y, outline=color, width=self.brush_size)
                self.draw.ellipse([self.start_x, self.start_y, end_x, end_y], outline=color, width=self.brush_size)
            elif self.drawing_tool == "line":
                self.canvas.create_line(self.start_x, self.start_y, end_x, end_y, fill=color, width=self.brush_size)
                self.draw.line([self.start_x, self.start_y, end_x, end_y], fill=color, width=self.brush_size)
            elif self.drawing_tool == "text":
                text = simpledialog.askstring("Text", "Enter the text:")
                if text:
                    self.canvas.create_text(self.start_x, self.start_y, text=text, fill=color, font=("Arial", self.brush_size * 2))
                    self.draw.text((self.start_x, self.start_y), text, fill=color)

    def choose_color(self):
        """Open a color chooser dialog."""
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color
            self.eraser_mode = False

    def toggle_eraser(self):
        """Toggle eraser mode."""
        self.eraser_mode = not self.eraser_mode
        self.brush_color = "white" if self.eraser_mode else self.brush_color

    def select_shape(self):
        """Select the drawing tool."""
        self.drawing_tool = self.shape_var.get()

    def select_brush_style(self):
        """Select the brush style."""
        self.brush_style = self.brush_style_var.get()

    def toggle_grid(self):
        """Toggle grid overlay on the canvas."""
        self.grid_visible = not self.grid_visible
        self.draw_grid()

    def draw_grid(self):
        """Draw or remove the grid overlay."""
        self.canvas.delete("grid")
        if self.grid_visible:
            step = 50
            for i in range(0, self.canvas_width, step):
                self.canvas.create_line(i, 0, i, self.canvas_height, fill="lightgray", tags="grid")
            for j in range(0, self.canvas_height, step):
                self.canvas.create_line(0, j, self.canvas_width, j, fill="lightgray", tags="grid")

    def gradient_background(self):
        """Fill the canvas with a gradient background."""
        color1 = colorchooser.askcolor(title="Choose Start Color")[1]
        color2 = colorchooser.askcolor(title="Choose End Color")[1]
        if color1 and color2:
            for i in range(self.canvas_height):
                ratio = i / self.canvas_height
                r = int(ratio * int(color2[1:3], 16) + (1 - ratio) * int(color1[1:3], 16))
                g = int(ratio * int(color2[3:5], 16) + (1 - ratio) * int(color1[3:5], 16))
                b = int(ratio * int(color2[5:7], 16) + (1 - ratio) * int(color1[5:7], 16))
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                self.canvas.create_line(0, i, self.canvas_width, i, fill=hex_color)
                self.draw.line([0, i, self.canvas_width, i], fill=hex_color)

    def resize_canvas(self):
        """Resize the canvas dimensions."""
        new_width = simpledialog.askinteger("Canvas Width", "Enter new canvas width:", minvalue=100, maxvalue=2000)
        new_height = simpledialog.askinteger("Canvas Height", "Enter new canvas height:", minvalue=100, maxvalue=2000)
        if new_width and new_height:
            self.canvas.config(width=new_width, height=new_height)
            self.canvas_width, self.canvas_height = new_width, new_height
            self.image = Image.new("RGB", (new_width, new_height), "white")
            self.draw = ImageDraw.Draw(self.image)
            self.clear_canvas()

    def clear_canvas(self):
        """Clear the canvas."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.undo_stack.clear()
        self.redo_stack.clear()
        if self.grid_visible:
            self.draw_grid()

    def save_canvas(self):
        """Save the canvas as an image."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Save", "Design saved successfully!")

    def undo(self):
        """Undo the last action."""
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.update_canvas()

    def redo(self):
        """Redo the last undone action."""
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.update_canvas()

    def update_canvas(self):
        """Update the canvas with the current image."""
        self.canvas.delete("all")
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesignApp(root)
    root.mainloop()
