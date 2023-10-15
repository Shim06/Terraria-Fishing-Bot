import customtkinter
import cv2
import json
from multiprocessing import Process, freeze_support, Event, Queue
import os
from pathlib import Path
from PIL import Image
import pyautogui
import threading
import time
import win32api


class App(customtkinter.CTk):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.stop_fishing_event = threading.Event()

        # configure window
        customtkinter.set_appearance_mode("dark") 
        customtkinter.set_default_color_theme(preferences["Color Theme"]) 
        self.title("Fishing Bot")
        self.iconbitmap('icon.ico')
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_columnconfigure(3, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.title = customtkinter.CTkLabel(self.sidebar_frame, text="Fishing Bot",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.start_button = customtkinter.CTkButton(self.sidebar_frame, text="Start",
                                                    command=self.start_button_event,
                                                    font=customtkinter.CTkFont(size=15))
        self.start_button.grid(row=1, column=0, padx=20, pady=10)

        self.stop_button = customtkinter.CTkButton(self.sidebar_frame, text="Stop",
                                                   command=self.stop_button_event, 
                                                   font=customtkinter.CTkFont(size=15))
        self.stop_button.grid(row=2, column=0, padx=20, pady=10)

        self.color_theme_label = customtkinter.CTkLabel(self.sidebar_frame, text="Color Theme:", anchor="w")
        self.color_theme_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.color_theme_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, 
                                                                       values=["Blue", "Dark-blue", "Green"],
                                                                       command=self.change_color_theme_event)
        self.color_theme_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create fishing log textbox
        self.log_textbox = customtkinter.CTkTextbox(self, width=250)
        self.log_textbox.grid(row=0, column=1, padx=(20, 0),
                          pady=20, sticky="nsew")

        # create options tabview
        self.options = customtkinter.CTkTabview(self, width=250)
        self.options.grid(row=0, column=2, padx=(20, 0),
                          pady=20, sticky="nsew")
        self.options.add("Options")
        self.options.tab("Options").grid_columnconfigure(0, weight=1)  
        optionsTab = self.options.tab("Options")

        self.catch_list_label = customtkinter.CTkLabel(optionsTab, text="Catch List",
                                                       font=customtkinter.CTkFont(
                                                       size=20, weight="bold"))
        self.catch_list_label.grid(row=0, column=0, padx=20)

        self.catches = customtkinter.CTkOptionMenu(optionsTab,
                                                  dynamic_resizing=False, values=[
                                                  "Advanced Combat Techniques", 
                                                  "Alchemy Table",
                                                  "Armored Cavefish",
                                                  "Atlantic Cod",
                                                  "Azure Crate",
                                                  "Balloon Pufferfish",
                                                  "Bass", "Bladetongue",
                                                  "Blue Jellyfish",
                                                  "Bomb Fish",
                                                  "Boreal Crate",
                                                  "Bottomless Lava Bucket",
                                                  "Bramble Crate", "Chaos Fish",
                                                  "Corrupt Crate",
                                                  "Crimson Crate",
                                                  "Crimson Tigerfish",
                                                  "Crystal Serpent",
                                                  "Damselfish", "Defiled Crate",
                                                  "Demon Conch", "Divine Crate",
                                                  "Double Cod",
                                                  "Dread of the Red Sea",
                                                  "Dungeon Crate", "Ebonkoi",
                                                  "Flarefin Koi","Flounder",
                                                  "Frog Leg", "Frost Daggerfish",
                                                  "Frost Minnow", "Frozen Crate",
                                                  "Golden Carp", "Golden Crate",
                                                  "Green Jellyfish",
                                                  "Hallowed Crate",
                                                  "Hellstone Crate",
                                                  "Hematic Crate", "Hemopiranha",
                                                  "Honeyfin", "Iron Crate",
                                                  "Joja Cola", "Jungle Crate",
                                                  "Lady of The Lake",
                                                  "Lava Absorbant Sponge",
                                                  "Mirage Crate",
                                                  "Mythril Crate", "Neon Tetra",
                                                  "Oasis Crate",
                                                  "Obsidian Crate",
                                                  "Obsidian Swordfish",
                                                  "Obsidifish", "Ocean Crate",
                                                  "Oyster", "Pearlwood Crate",
                                                  "Pink Jellyfish",
                                                  "Princess Fish","Prismite",
                                                  "Purple Clubberfish",
                                                  "Reaver Shark", "Red Snapper",
                                                  "Rockfish", "Rock Lobster",
                                                  "Salmon", "Sawtooth Shark",
                                                  "Scaly Truffle",
                                                  "Seaside Crate", "Shrimp",
                                                  "Sky Crate", "Specular Fish",
                                                  "Stinkfish", "Stockade Crate",
                                                  "Swordfish", "Titanium Crate",
                                                  "Toxikarp", "Trout", "Tuna",
                                                  "Variegated Lardfish",
                                                  "Wooden Crate", "Zephyr Fish"])
        self.catches.grid(row=1, column=0, padx=20, pady=(5, 0))

        self.selected_catches = customtkinter.CTkTextbox(optionsTab, height=215)
        self.selected_catches.grid(row=2, column=0, padx=(10), pady=(10, 0), sticky="nsew")

        self.add_button = customtkinter.CTkButton(optionsTab, text="Add",
                                                  command=self.add_button_event)
        self.add_button.grid(row=3, column=0, padx=(40),
                             pady=(10, 0), sticky="nsew")
        
        self.clear_button = customtkinter.CTkButton(optionsTab, text="Clear",
                                                    command=self.clear_button_event)
        self.clear_button.grid(row=4, column=0, padx=(40), pady=(10, 0), sticky="nsew")

        self.remember_list_switch = customtkinter.CTkSwitch(optionsTab, text="Remember catch list",
                                                            command=self.save_switch_preferences)
        self.remember_list_switch.grid(row=5, column=0, padx=(10), pady=(15, 0), sticky="nsew")

        self.auto_drink_switch = customtkinter.CTkSwitch(optionsTab, text="Auto drink potion",
                                                         command=self.save_switch_preferences)
        self.auto_drink_switch.grid(row=6, column=0, padx=(10), pady=(15, 0), sticky="nsew")

        self.grayscale_switch = customtkinter.CTkSwitch(optionsTab, text="Grayscale",
                                                         command=self.save_switch_preferences)
        self.grayscale_switch.grid(row=7, column=0, padx=(10), pady=(15, 0), sticky="nsew")

        if preferences["remember list"] == True:
            self.remember_list_switch.select()
        else:
            self.remember_list_switch.deselect()
        if preferences["auto drink"] == True:
            self.auto_drink_switch.select()
        else:
            self.auto_drink_switch.deselect()
        if preferences["grayscale"] == True:
            self.grayscale_switch.select()
        else:
            self.grayscale_switch.deselect()

        # Fishing Statistics
        self.statistics_frame = customtkinter.CTkScrollableFrame(self, width=250)
        self.statistics_frame.grid_columnconfigure(0, weight=1)
        self.statistics_frame.grid_rowconfigure(1, weight=1)
        self.statistics_frame.grid(row=0, column=3, padx=(20, 20), pady=(20), sticky="nsew")
        self.statisticsLabel = customtkinter.CTkLabel(self.statistics_frame, text="Statistics", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.statisticsLabel.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="nsew")

        self.statistics_view = customtkinter.CTkTabview(self.statistics_frame)
        self.statistics_view.configure(fg_color="#333333")
        self.statistics_view.grid(row=1, column=0, padx=(10, 0), pady=(0, 20), sticky="nsew")
        self.statistics_view.add("Fish")
        self.statistics_view.add("Quest Fish")
        self.statistics_view.add("Usable Items")
        self.statistics_view.add("Crates")

        self.statistics_view.tab("Fish").grid_columnconfigure(0, weight=1)  
        self.statistics_view.tab("Quest Fish").grid_columnconfigure(0, weight=1) 
        self.statistics_view.tab("Usable Items").grid_columnconfigure(0, weight=1) 
        self.statistics_view.tab("Crates").grid_columnconfigure(0, weight=1) 

        # Set default values
        self.stop_button.configure(state="disabled")
        self.selected_catches.configure(state="disabled")
        self.color_theme_optionemenu.set(preferences["Color Theme"].capitalize())
        self.scaling_optionemenu.set("100%")
        self.catches.set("Catches")
        self.log_textbox.insert("0.0", "Fishing Log\n\n")
        self.log_textbox.configure(state="disabled")

        if self.remember_list_switch.get() == 1:
            for string in preferences["Catch List"]:
                self.selected_catches.configure(state="normal")
                self.selected_catches.insert("end", f"{string}\n")
                self.selected_catches.configure(state="disabled")
        else:
            preferences["Catch List"] = []
            with open(preferences_json, "w") as f:
                json.dump(preferences, f, indent=4)
        
        # Fish statistics tab
        self.statistics_label = []
        self.statistics_view_fish_label = customtkinter.CTkLabel(self.statistics_view.tab("Fish"),
                                                                 text="Number of Catches:",
                                                                 font=("TkDefaultFont", 15))
        self.statistics_view_fish_label.grid(row=0, column=0,
                                             padx=20, pady=0)
        
        for i, (catch, value) in enumerate(statistics_data["Fish"].items()):
            self.statistics_view_label = customtkinter.CTkLabel(self.statistics_view.tab("Fish"),
                                                                    text=f"{catch}: {value}",
                                                                    font=("TkDefaultFont", 12),)
            self.statistics_view_label.grid(row=i + 1, column=0,
                                                  sticky="w")
            self.statistics_label.append(self.statistics_view_label)

        # Quest Fish statistics tab
        self.statistics_label2 = []
        self.statistics_view_label = customtkinter.CTkLabel(self.statistics_view.tab("Quest Fish"),
                                                                 text="Number of Catches:",
                                                                 font=("TkDefaultFont", 15))
        self.statistics_view_label.grid(row=0, column=0,
                                        padx=20, pady=0)
        
        for i, (catch, value) in enumerate(statistics_data["Quest Fish"].items()):
            self.statistics_view_label_2 = customtkinter.CTkLabel(self.statistics_view.tab("Quest Fish"),
                                                                    text=f"{catch}: {value}",
                                                                    font=("TkDefaultFont", 12),)
            self.statistics_view_label_2.grid(row=i + 1, column=0,
                                              sticky="w")
            self.statistics_label2.append(self.statistics_view_label_2)

        # Usable Items statistics tab
        self.statistics_label3 = []
        self.statistics_view_label3 = customtkinter.CTkLabel(self.statistics_view.tab("Usable Items"),
                                                                 text="Number of Catches:",
                                                                 font=("TkDefaultFont", 15))
        self.statistics_view_label3.grid(row=0, column=0,
                                        padx=20, pady=0)
        
        for i, (catch, value) in enumerate(statistics_data["Usable Items"].items()):
            self.statistics_view_label_3 = customtkinter.CTkLabel(self.statistics_view.tab("Usable Items"),
                                                                    text=f"{catch}: {value}",
                                                                    font=("TkDefaultFont", 12),)
            self.statistics_view_label_3.grid(row=i + 1, column=0,
                                              sticky="w")
            self.statistics_label3.append(self.statistics_view_label_3)

        # Crates statistics tab
        self.statistics_label4 = []
        self.statistics_view_label4 = customtkinter.CTkLabel(self.statistics_view.tab("Crates"),
                                                                 text="Number of Catches:",
                                                                 font=("TkDefaultFont", 15))
        self.statistics_view_label4.grid(row=0, column=0,
                                         padx=20, pady=0)
        
        for i, (catch, value) in enumerate(statistics_data["Crates"].items()):
            self.statistics_view_label_4 = customtkinter.CTkLabel(self.statistics_view.tab("Crates"),
                                                                    text=f"{catch}: {value}",
                                                                    font=("TkDefaultFont", 12),)
            self.statistics_view_label_4.grid(row=i + 1, column=0,
                                             sticky="w")
            self.statistics_label4.append(self.statistics_view_label_4)
            
    def update_statistics(self):
        for i, (catch, value) in enumerate(statistics_data["Fish"].items()):
            self.statistics_label[i].configure(text=f"{catch}: {value}")

        for i, (catch, value) in enumerate(statistics_data["Quest Fish"].items()):
            self.statistics_label2[i].configure(text=f"{catch}: {value}")

        for i, (catch, value) in enumerate(statistics_data["Usable Items"].items()):
            self.statistics_label3[i].configure(text=f"{catch}: {value}")
        
        for i, (catch, value) in enumerate(statistics_data["Crates"].items()):
            self.statistics_label4[i].configure(text=f"{catch}: {value}")
           

    def change_color_theme_event(self, new_color_theme: str):
        customtkinter.set_default_color_theme(new_color_theme.lower())
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{new_color_theme} color theme has been selected. \n")
        self.log_textbox.insert("end", "Restart application to apply new theme. \n\n")
        self.log_textbox.configure(state="disabled")

        preferences["Color Theme"] = new_color_theme.lower()
        with open(preferences_json, "w") as f:
            json.dump(preferences, f, indent=4)


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def start_button_event(self):
        if self.selected_catches.get("0.0") != "\n":
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.add_button.configure(state="disabled")
            self.clear_button.configure(state="disabled")
            self.stop_fishing_event.clear()
            bot.stop_event.clear()

            self.thread = threading.Thread(target=self.choose_fishing_location, args=(queue,))
            self.thread.daemon = True
            self.thread.start()
        
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", "Waiting for fishing location...\n")
            self.log_textbox.insert("end", "Right click to select... \n")
            self.log_textbox.configure(state="disabled")
            self.save_switch_preferences()
            
        else:
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", "No catches selected...\n")
            self.log_textbox.insert("end", "Please select. \n")
            self.log_textbox.configure(state="disabled")

    def stop_button_event(self):
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.add_button.configure(state="normal")
        self.clear_button.configure(state="normal")
        bot.stop_event.set()
        self.stop_fishing_event.set()
        bot.clear_fish_list()

        self.save_switch_preferences()
        
    def add_button_event(self):
        lines = self.selected_catches.get("0.0", "end").count("\n")
        for line in range(lines):
            lineNumber = str(line)
            lineText = self.selected_catches.get(lineNumber + ".0", lineNumber + ".end")
            text = text=self.catches.get()
            if (text == lineText or text == "Catches"):
                selectText = False
                return
            else:
                selectText = True

        if selectText == True:
            self.selected_catches.configure(state="normal")
            self.selected_catches.insert("end", text=text + "\n")
            self.selected_catches.configure(state="disabled")

        # Saves list
        self.catch_list = []
        for i in self.selected_catches.get("0.0", "end").splitlines():  
            if i != "":
                self.catch_list.append(i)
        preferences["Catch List"] = self.catch_list
        with open(preferences_json, "w") as f:
            json.dump(preferences, f, indent=4)

    def clear_button_event(self):
        # Clears list
        self.selected_catches.configure(state="normal")
        self.selected_catches.delete("0.0", "end")
        self.selected_catches.configure(state="disabled")

        preferences["Catch List"] = []
        with open(preferences_json, "w") as f:
            json.dump(preferences, f, indent=4)

    # Waits and returns pixel location of mouse when pressing right click
    def choose_fishing_location(self, queue):
        while True:
            if win32api.GetKeyState(0x02) < 0:
                x, y = win32api.GetCursorPos()

                self.log_textbox.configure(state="normal")
                self.log_textbox.insert("end", f"Fishing location at {x}, {y}.\n\n")
                self.log_textbox.configure(state="disabled")
                self.start_fishing(x, y, preferences["grayscale"])

                if preferences["auto drink"] == True:
                    process2 = Process(target=bot.auto_drink, args=(start_time,))
                    process2.daemon = True
                    process2.start()

                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()
                return
            
            if self.stop_fishing_event.is_set():
                return

    def start_fishing(self, x:int, y:int, grayscale: bool):
        catch_list = self.selected_catches.get("0.0", "end")
        create_fish_list_process = Process(
                                    target=bot.create_fish_list(
                                    catch_list, images_path))
        create_fish_list_process.daemon = True
        create_fish_list_process.start()
        create_fish_list_process.join()
        fish_process = Process(target=bot.fish,
                               args=(True, x, y, 
                                     grayscale))
        fish_process.daemon = True
        fish_process.start()

    def process_queue_data(self, queue):
        while True:
            data = queue.get()
            app.log_textbox.configure(state="normal")
            app.log_textbox.insert("end", f"Caught {data}.\n")
            app.log_textbox.configure(state="disabled")
            for key in statistics_data.keys():
                if data in statistics_data[key]:

                    # Increments caught catch by 1 in statistics 
                    statistics_data[key][data] += 1
                    self.update_statistics()

                    # Saves statistics
                    with open(statistics_json, "w") as f:
                        json.dump(statistics_data, f, indent=4)
                    break

    def save_switch_preferences(self):
        switch1 = self.remember_list_switch.get()
        switch2 = self.auto_drink_switch.get()
        switch3 = self.grayscale_switch.get()

        if switch1 == 1:
            preferences["remember list"] = True
        else:
            preferences["remember list"] = False
        
        if switch2 == 1:
            preferences["auto drink"] = True
        else:
            preferences["auto drink"] = False

        if switch3 == 1:
            preferences["grayscale"] = True
        else:
            preferences["grayscale"] = False

        with open (preferences_json, "w") as f:
            json.dump(preferences, f, indent=4)
        

class FishingBot():
    def __init__(self, queue):
        super().__init__()
        self.fish_list = []
        self.images = []
        self.image_scale = (1920, 1080)
        self.current_monitor_size = pyautogui.size()  # Get the current Monitor Size
        self.catching = False
        self.stop_event = Event()
        self.queue = queue

    def fish(self, fishing: bool, x:int, y:int, preferences: bool):
        while fishing and not self.stop_event.is_set():
            if self.catching != True:
                for i, img in enumerate(self.images):
                    catch = pyautogui.locateOnScreen(img, confidence=0.55,
                                                     grayscale=preferences)
                    if catch is not None:
                        self.catching = True
                        pyautogui.moveTo(x, y)
                        pyautogui.mouseDown()
                        time.sleep(0.1)
                        pyautogui.mouseUp()
                        time.sleep(1.5)
                        pyautogui.mouseDown()
                        time.sleep(0.1)
                        pyautogui.mouseUp()
                        
                        name_without_path = os.path.basename(self.fish_list[i])
                        name = os.path.splitext(name_without_path)[0]
                        self.queue.put(name)

                        self.catching = False

                    if self.stop_event.is_set():
                        break
            time.sleep(0.2)

    # Creates an image list for the selected catches
    def create_fish_list(self, selected: str, path):
        for line in selected.splitlines():
            if line != "":
                img_path = path.joinpath(f"{line}.png")
                self.fish_list.append(img_path)
                image = Image.open(img_path)
                self.images.append(image)

        for i, catch in enumerate(self.images):
            # Scales the images according to current monitor screen size
            if self.current_monitor_size != self.image_scale:
                img_scale_x, img_scale_y = (int(catch.size[0] *
                                            (self.current_monitor_size[0] / self.image_scale[0])),
                                            int(catch.size[1] *
                                            (self.current_monitor_size[1] / self.image_scale[1])))
                self.images[i] = catch.resize((img_scale_x, img_scale_y))
                
            
    def clear_fish_list(self):
        self.fish_list = []
        self.images = []

    # Automatically drinks potions every 1 minutes
    def auto_drink(self, current_time):
        while True:
            pyautogui.keyDown("b")
            time.sleep(0.1)
            pyautogui.keyUp("b")
            time.sleep(61.0 - ((time.monotonic() - current_time) % 61.0))

            if self.stop_event.is_set():
                return


if __name__ == "__main__": 
    freeze_support()

    path = Path(".")
    images_path = path / "images"
    statistics_json = path.joinpath("statistics.json")
    preferences_json = path.joinpath("preferences.json")

    with open(statistics_json) as f:
        statistics_data = json.load(f)
    with open(preferences_json) as f:
        preferences = json.load(f)

    queue = Queue()
    app = App(queue)
    bot = FishingBot(queue)
    start_time = time.monotonic()
    
    queue_thread = threading.Thread(target=app.process_queue_data, args=(queue,))
    queue_thread.daemon = True
    queue_thread.start()
    
    app.update_statistics()
    app.mainloop()