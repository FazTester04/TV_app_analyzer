import json
import os
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

def build_flow_gui():
    root = tk.Tk()
    root.withdraw()  # hide root window

    flow_data = {"steps": []}
    messagebox.showinfo("Flow Builder", "Let's build your test flow!")

    while True:
        action = simpledialog.askstring(
            "Action",
            "Enter action (power_on, launch_app, play, wait, check_status, or 'done'):"
        )
        if not action or action.lower() == "done":
            break

        step = {"action": action}

        if action == "launch_app":
            step["app"] = simpledialog.askstring("App Name", "Enter app name:")
        elif action == "play":
            step["title"] = simpledialog.askstring("Title", "Enter title to play:")
        elif action == "wait":
            step["seconds"] = simpledialog.askinteger("Wait", "How many seconds to wait?")
        elif action == "check_status":
            step["expect"] = simpledialog.askstring("Expect", "Expected status (App loaded / Playing):")

        flow_data["steps"].append(step)

    if not flow_data["steps"]:
        messagebox.showinfo("Flow Builder", "No steps added.")
        return

    save_path = filedialog.asksaveasfilename(
        title="Save Flow JSON",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        initialdir=os.path.join(os.getcwd(), "flows")
    )

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(flow_data, f, indent=4)
        messagebox.showinfo("Flow Builder", f"Flow saved to {save_path}")
    else:
        messagebox.showinfo("Flow Builder", "Flow not saved.")


if __name__ == "__main__":
    build_flow_gui()
