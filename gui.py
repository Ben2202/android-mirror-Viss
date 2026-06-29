import customtkinter as ctk
import tkinter as tk

from devices import detect_devices
from mirror import start_mirror
from sync import start_sync


class MirrorGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("Android Mirror Manager")
        self.geometry("1000x720")

        self.devices = []
        self.label_to_device = {}
        self.follow_vars = {}

        self.master_var = tk.StringVar(value="Geen apparaten")

        title = ctk.CTkLabel(
            self,
            text="Android Mirror Manager",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)

        self.status = ctk.CTkLabel(
            self,
            text="Klik op Detect Devices"
        )
        self.status.pack()

        ctk.CTkLabel(
            self,
            text="⭐ Master Device",
            font=("Arial", 20, "bold")
        ).pack(pady=(20,5))

        self.master_menu = ctk.CTkOptionMenu(
            self,
            variable=self.master_var,
            values=["Geen apparaten"]
        )
        self.master_menu.pack()

        ctk.CTkLabel(
            self,
            text="📱 Followers",
            font=("Arial",20,"bold")
        ).pack(pady=(20,5))

        self.follow_frame = ctk.CTkScrollableFrame(
            self,
            width=800,
            height=300
        )
        self.follow_frame.pack(padx=20,pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Detect Devices",
            command=self.refresh_devices
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Open Mirrors",
            command=self.open_mirrors
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Start Sync",
            command=self.start_sync_button
        ).pack(side="left", padx=10)

    def refresh_devices(self):

        self.devices = detect_devices()

        self.label_to_device.clear()
        self.follow_vars.clear()

        for widget in self.follow_frame.winfo_children():
            widget.destroy()

        if not self.devices:
            self.status.configure(text="Geen apparaten gevonden")
            return

        labels = []

        for device in self.devices:

            label = f"{device['model']} ({device['serial']})"

            labels.append(label)

            self.label_to_device[label] = device

        self.master_menu.configure(values=labels)
        self.master_var.set(labels[0])

        for label in labels:

            serial = self.label_to_device[label]["serial"]

            var = tk.BooleanVar(value=True)

            self.follow_vars[serial] = var

            ctk.CTkCheckBox(
                self.follow_frame,
                text=label,
                variable=var
            ).pack(anchor="w", padx=10, pady=5)

        self.status.configure(text=f"{len(labels)} apparaten gevonden")

    def open_mirrors(self):

        opened = []

        master = self.label_to_device[self.master_var.get()]["serial"]

        opened.append(master)

        for serial, var in self.follow_vars.items():

            if serial != master and var.get():
                opened.append(serial)

        for serial in opened:
            start_mirror(serial)

        self.status.configure(text=f"{len(opened)} mirrors geopend")

    def start_sync_button(self):

        master = self.label_to_device[self.master_var.get()]["serial"]

        followers = []

        for serial, var in self.follow_vars.items():

            if serial != master and var.get():
                followers.append(serial)

        start_sync(master, followers)

        self.status.configure(text="Sync gestart")