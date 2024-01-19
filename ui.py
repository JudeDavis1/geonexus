import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext

import customtkinter as ctk

from src.distance import get_distance_map


class GeonexApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Geonex App")
        self.geometry("700x500")

        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_forever)
        self.thread.start()

        # Header label
        self.header_label = ctk.CTkLabel(self, text="Calculate Road Distances")
        self.header_label.text_font = ("Arial", 16)
        self.header_label.pack(pady=20)

        # Target road label and entry
        self.target_road_label = ctk.CTkLabel(self, text="Target Road Name:")
        self.target_road_label.pack(pady=5)
        self.target_road_entry = ctk.CTkEntry(
            self, placeholder_text="e.g., Northern Road, Slough, UK", width=300
        )
        self.target_road_entry.pack(pady=5)

        # Progress bar (indeterminate)
        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress_bar.pack(pady=5)
        self.progress_bar.pack_forget()

        # Calculate button
        self.calculate_button = ctk.CTkButton(
            self, text="Calculate", command=self.calculate_distances
        )
        self.calculate_button.pack(pady=20)

        # Results scrolled text area
        self.results_text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, height=15, width=60
        )
        self.results_text.pack(pady=10, fill="both", expand=True)

        # Clear button
        self.clear_button = ctk.CTkButton(
            self, text="Clear Results", command=self.clear_results
        )
        self.clear_button.pack(pady=5)

    def calculate_distances(self):
        self.progress_bar.pack(pady=5)  # Show the progress bar
        self.progress_bar.start()

        target_road_name = self.target_road_entry.get()
        asyncio.run(self.calculate_distances_routine(target_road_name))

    async def calculate_distances_routine(self, target_road_name):
        if target_road_name:
            distance_map = await get_distance_map(target_road_name)
            self.loop.call_soon_threadsafe(self.display_results, distance_map)
        else:
            self.loop.call_soon_threadsafe(
                self.results_text.insert, tk.END, "Please enter a target road name.\n"
            )

        self.loop.call_soon_threadsafe(self.stop_progress_bar)

    def stop_progress_bar(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def display_results(self, distance_map):
        self.results_text.delete("1.0", tk.END)
        sorted_results = sorted(distance_map.items(), key=lambda item: item[1])

        for road, distance in sorted_results[:10]:
            self.results_text.insert(tk.END, f"{road}: {distance:.2f} miles\n")

    def clear_results(self):
        self.results_text.delete("1.0", tk.END)


if __name__ == "__main__":
    app = GeonexApp()
    app.mainloop()
