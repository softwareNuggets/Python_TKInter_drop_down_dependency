import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json





class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.title('Drop-down Combo with Dependencies')
        
        with open("locations.json","r") as file:
            self.data = json.load(file)

        # Define the country, state, and city as a StringVar object variable
        # you can access the value inside of a StringVar object using the .get() function
        # StringVar provides easy way to link: value to widgets in the GUI
        self.country_var = tk.StringVar()
        self.state_var = tk.StringVar()
        self.city_var = tk.StringVar()
        
        # Create the country label and dropdown combo and ComboboxSelected event
        ttk.Label(root, text="Country:").grid(row=0, column=0, padx=10, pady=10)
        self.country_combo = ttk.Combobox(root, textvariable=self.country_var, state="readonly")
        self.country_combo.grid(row=0, column=1, padx=10, pady=10)
        self.country_combo.bind("<<ComboboxSelected>>", self.update_states)
        self.country_combo.set("Select a Country")
        
        # Create the state label and dropdown combo and ComboboxSelected event
        ttk.Label(root, text="State:").grid(row=1, column=0, padx=10, pady=10)
        self.state_combo = ttk.Combobox(root, textvariable=self.state_var, state="readonly")
        self.state_combo.grid(row=1, column=1, padx=10, pady=10)
        self.state_combo.bind("<<ComboboxSelected>>", self.update_cities)
       
        # Create the city label and dropdown combo and ComboboxSelected event
        ttk.Label(root, text="City:").grid(row=2, column=0, padx=10, pady=10)
        self.city_combo = ttk.Combobox(root, textvariable=self.city_var, state="readonly")
        self.city_combo.grid(row=2, column=1, padx=10, pady=10)
        
        # Update the list of countries in the country dropdown combo
        self.update_countries()
        
        # Show a message in the state and city dropdowns indicating that a country must be selected first
        self.state_combo.set("Select a Country First")
        self.city_combo.set("Select a Country First")

        # relief = 'flat','raised','sunken','groove','ridge'
        # Create Submit button
        self.submit_button = tk.Button(root, text="Submit", 
                                            relief="groove",
                                            bg='LightGreen',
                                            activebackground='White',
                                            command=self.print_selected)
        self.submit_button.grid(row=3,column=1,pady=10)

        # Create Clear button
        self.clear_button = tk.Button(root, text="Clear", 
                                        relief='groove',
                                        command=self.clear_selection)
        self.clear_button.grid(row=3,column=2,pady=10)


    def print_selected(self):
        country = self.country_var.get()
        state = self.state_var.get()
        city = self.city_var.get()

        # Check if all three combo boxes have been selected
        if (country in ["Select a Country First", "Select Country","Select a Country"] or
            state in ["Select State","Select A State", "Select Country","Select a Country First"] or
            city in ["Select City", "Select A City", "Select a State","Select Country", 
                    "Select Country and State First"]):
        
            # Show an error message if any of the combo boxes are not selected
            messagebox.showerror("Error", "Please select a value for all three combo boxes.")
            return

        strLocation = f"Selected: Country={country}, City={city}, State={state}"
        messagebox.showinfo("Selected Location",strLocation)
        

    def clear_selection(self):
        self.country_var.set("Select Country")
        self.state_var.set("Select a Country")
        self.city_var.set("Select a Country")
        countries = list(self.data.keys())
        
        self.country_combo["values"] = countries;
        self.state_combo["values"]  = []
        self.city_combo["values"]   = []


    def update_countries(self):
        countries = list(self.data.keys())
        self.state_combo["values"]  = []
        self.city_combo["values"]   = []
        self.country_combo["values"] = countries
        
        
    def update_states(self, *args):
        # Get the selected country from the country dropdown combo
        country = self.country_var.get()
        
        # create list containing the country values
        keys = list(self.data.keys())

        # Check if the selected country is a valid key in the data dictionary
        if country not in keys:
            # Clear the state and city dropdowns and return early if the country is not valid
            self.state_var.set('Select a Country')
            self.city_var.set('Select a Country')
            self.state_combo["values"]  = []
            self.city_combo["values"]   = []
            return
        
        # Get the list of states for the selected country
        states = sorted(list(self.data[country].keys()))
        
        # Update the state dropdown combo with the list of states
        self.state_combo.config(values=states)
        self.city_combo["values"]   = []
        
        # Clear the selected state and city variables
        self.state_var.set('Select State')
        self.city_var.set('Select a State')
        
        # Update the list of cities based on the currently selected country and state
        self.update_cities()

        
    def update_cities(self, *args):
        # Get the selected state from the state dropdown combo
        state = self.state_var.get()
        
        if (state in ["Select State", "Select a State"]):
            self.city_var.set('Select a State')
            return

        #let's get a list of states, whom parent is self.country_var.get()
        country_name = self.country_var.get();
        states_in_country = list(self.data.get(country_name))

        # Check if the selected state is valid for the current country
        if state not in states_in_country:
        #if state not in self.data.get(self.country_var.get(), {}):
            # Clear the city dropdown combo and the city variable if the selected state is not valid
            self.city_var.set('')
            self.city_combo = []
            return
        
        # Get the list of cities for the selected state and country
        cities = sorted(self.data[country_name][state])
        
        # Update the city dropdown combo with the list of cities
        self.city_combo.config(values=cities)
        
        # Clear the selected city variable
        self.city_var.set("Select City")


# Create the Tkinter window and run the app
root = tk.Tk()
app = App(root)
root.mainloop()
