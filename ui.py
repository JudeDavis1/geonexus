import asyncio
import threading
import tkinter as tk
import tkinter.ttk as ttk

import customtkinter as ctk

from src.distance import get_distance_map


class GeonexApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Geonex App")
        self.geometry("700x700")

        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_forever)
        self.thread.start()

        # Header label
        self.header_label = ctk.CTkLabel(self, text="Calculate Road Distances")
        self.header_label.text_font = ("Arial", 16)
        self.header_label.pack(pady=20)

        # Progress bar (indeterminate)
        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress_bar.pack(pady=5)
        self.progress_bar.pack_forget()

        # Target road label and entry
        self.target_road_label = ctk.CTkLabel(self, text="Target Road Name:")
        self.target_road_label.pack(pady=5)
        self.target_road_entry = ctk.CTkEntry(
            self, placeholder_text="e.g., Northern Road, Slough, UK", width=300
        )
        self.target_road_entry.pack(pady=5)

        # Calculate button
        self.calculate_button = ctk.CTkButton(
            self, text="Calculate", command=self.calculate_distances
        )
        self.calculate_button.pack(pady=20)

        # Results scrolled text area
        self.results_table = ttk.Treeview(
            self, columns=("Road", "Distance"), show="headings"
        )
        self.results_table.heading("Road", text="Road")
        self.results_table.heading("Distance", text="Distance (miles)")
        self.results_table.column("Road", anchor=tk.W)
        self.results_table.column("Distance", anchor=tk.E)
        self.results_table.pack(pady=10, fill="both", expand=True)

        # Clear button
        self.clear_button = ctk.CTkButton(
            self, text="Clear Results", command=self.clear_results
        )
        self.clear_button.pack(pady=5)

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#22559b")])

        style.configure(
            "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
        )
        style.map("Treeview.Heading", background=[("active", "#3484F0")])

    def calculate_distances(self):
        self.progress_bar.pack(pady=5)  # Show the progress bar
        self.progress_bar.start()

        target_road_name = self.target_road_entry.get()
        coroutine = self.calculate_distances_routine(target_road_name)
        asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    async def calculate_distances_routine(self, target_road_name):
        if target_road_name:
            distance_map = None
            try:
                distance_map = await get_distance_map(target_road_name)
            except:
                pass
            self.loop.call_soon_threadsafe(self.display_results, distance_map)
        else:
            self.loop.call_soon_threadsafe(
                self.results_table.insert, tk.END, "Please enter a target road name.\n"
            )

        self.loop.call_soon_threadsafe(self.stop_progress_bar)

    def stop_progress_bar(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def display_results(self, distance_map):
        self.results_table.delete(
            *self.results_table.get_children()
        )  # Clear existing data

        if distance_map is None:
            return  # Display nothing if no results

        sorted_results = sorted(distance_map.items(), key=lambda item: item[1])
        for road, distance in sorted_results[:10]:
            self.results_table.insert("", tk.END, values=(road, f"{distance:.2f}"))

    def clear_results(self):
        for item in self.results_table.get_children():
            self.results_table.delete(item)


if __name__ == "__main__":
    app = GeonexApp()
    app.mainloop()
