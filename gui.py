import customtkinter as ctk
import tkinter as tk

from devices import detect_devices
from mirror import start_mirror
from sync import start_sync, stop_sync


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
        self.device_columns = 3

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
            width=860,
            height=300
        )
        self.follow_frame.pack(padx=20, pady=10, fill="both", expand=True)

        for column in range(self.device_columns):
            self.follow_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="device_cards"
            )

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20, padx=20, fill="x")

        for column in range(4):
            button_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="action_buttons"
            )

        buttons = (
            ("Detect Devices", self.refresh_devices),
            ("Open Mirrors", self.open_mirrors),
            ("Start Sync", self.start_sync_button),
            ("Stop Sync", self.stop_sync_button),
        )

        for column, (text, command) in enumerate(buttons):
            ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=160
            ).grid(row=0, column=column, padx=8, pady=10, sticky="ew")

    def refresh_devices(self):

        self.devices = detect_devices()

        self.label_to_device.clear()
        self.follow_vars.clear()

        for widget in self.follow_frame.winfo_children():
            widget.destroy()

        if not self.devices:
            self.status.configure(text="Geen apparaten gevonden")
            # Reset option menu to default state
            self.master_menu.configure(values=["Geen apparaten"])
            self.master_var.set("Geen apparaten")
            return

        labels = []

        for device in self.devices:

            label = f"{device['model']} ({device['serial']})"

            labels.append(label)

            self.label_to_device[label] = device

        self.master_menu.configure(values=labels)
        if labels:
            self.master_var.set(labels[0])

        for index, label in enumerate(labels):

            serial = self.label_to_device[label]["serial"]

            var = tk.BooleanVar(value=True)

            self.follow_vars[serial] = var

            row = index // self.device_columns
            column = index % self.device_columns

            device_card = ctk.CTkFrame(
                self.follow_frame,
                width=260,
                height=68
            )
            device_card.grid(
                row=row,
                column=column,
                padx=8,
                pady=8,
                sticky="nsew"
            )
            device_card.grid_propagate(False)
            device_card.grid_columnconfigure(0, weight=1)

            ctk.CTkCheckBox(
                device_card,
                text=label,
                variable=var,
                width=220
            ).grid(row=0, column=0, padx=12, pady=18, sticky="w")

        self.status.configure(text=f"{len(labels)} apparaten gevonden")

    def open_mirrors(self):

        opened = []

        master_label = self.master_var.get()

        if master_label not in self.label_to_device:
            self.status.configure(text="Geen master geselecteerd")
            return

        master = self.label_to_device[master_label]["serial"]

        opened.append(master)

        for serial, var in self.follow_vars.items():

            if serial != master and var.get():
                opened.append(serial)

        for serial in opened:
            start_mirror(serial)

        self.status.configure(text=f"{len(opened)} mirrors geopend")

    def start_sync_button(self):

        master_label = self.master_var.get()

        if master_label not in self.label_to_device:
            self.status.configure(text="Geen master geselecteerd")
            return

        master = self.label_to_device[master_label]["serial"]

        followers = []

        for serial, var in self.follow_vars.items():

            if serial != master and var.get():
                followers.append(serial)

        if not followers:
            self.status.configure(text="Geen volgers geselecteerd")
            return

        if not start_sync(master, followers):
            self.status.configure(text="Sync draait al")
            return

        self.status.configure(text="Sync gestart")

    def stop_sync_button(self):

        if stop_sync():
            self.status.configure(text="Sync gestopt")
        else:
            self.status.configure(text="Geen sync actief")
