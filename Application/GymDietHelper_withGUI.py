import pickle
from tkinter import *
from typing import Tuple
import customtkinter
from tkinter import simpledialog
from tkinter import messagebox
import os

# Define the file path
file_path = "data.pkl"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GymDietHelper")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        customtkinter.set_appearance_mode("dark")
    
    def createData(self):
        messagebox.showinfo("No Data yet", "No Data yet. We will fill it together!")
        Weight = simpledialog.askfloat("Input", "What is your current weight in kg:")
        Calories = simpledialog.askinteger("Input", "What is your daily calorie intake in kcal:")
        diet = simpledialog.askstring("Input", "What is your diet? (Bulking[b]/Cutting[c]/Maintenance[m]):")
        return [Weight, Calories, diet]

    def showDataFile1(self, day, weight, calorie, diet, currentWeight, currentCalorie, analyst, weightdiff):
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=1, columnspan=4, padx=10, pady=10, sticky="")
        self.label = customtkinter.CTkLabel(self.frame, text=("Day: " + str(day)))
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="nwse")
        self.label = customtkinter.CTkLabel(self.frame, text=("Startweight: " + weight + " kg"))
        self.label.grid(row=1, column=1, padx=10, pady=10, sticky="nwse")
        self.label = customtkinter.CTkLabel(self.frame, text=("Daily Calorie Intake: " + calorie + " kcal"))
        self.label.grid(row=1, column=2, padx=10, pady=10, sticky="nwse")
        self.label = customtkinter.CTkLabel(self.frame, text=("Diet: " + diet))
        self.label.grid(row=1, column=3, padx=10, pady=10, sticky="nwse")
        if(currentWeight and currentCalorie and analyst and weightdiff != 0):
            self.frame2 = customtkinter.CTkFrame(self)
            self.frame2.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="")
            self.label = customtkinter.CTkLabel(self.frame2, text=("Weight " + str(currentWeight)+ " kg"))
            self.label.grid(row=2, column=0, padx=10, pady=10, sticky="nwse")
            self.label = customtkinter.CTkLabel(self.frame2, text=("Calorie: " + currentCalorie + " kcal"))
            self.label.grid(row=2, column=1, padx=10, pady=10, sticky="nwse")
            self.label = customtkinter.CTkLabel(self, text=(analyst))
            self.label.grid(row=0, column=0 , columnspan=4, padx=10, pady=10, sticky="nwse")
            self.label = customtkinter.CTkLabel(self.frame2, text=("Weekly weight differnce: " + weightdiff))
            self.label.grid(row=2, column=2, padx=10, pady=10, sticky="nwse")

    def showbutton(self):
        self.buttonGData = customtkinter.CTkButton(self, text="Change Global Data", command=self.buttonGData_callback)
        self.buttonGData.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.buttonDData = customtkinter.CTkButton(self, text="Add Daily Data", command=self.buttonDData_callback)
        self.buttonDData.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.buttonCDData = customtkinter.CTkButton(self, text="Change Daily Data", command=self.buttonCDData_callback)
        self.buttonCDData.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.buttonDDData = customtkinter.CTkButton(self, text="Delete Daily Data", command=self.buttonDDData_callback)
        self.buttonDDData.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.buttonSData = customtkinter.CTkButton(self, text="Show Daily Data", command=self.buttonSData_callback)
        self.buttonSData.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.buttonSData = customtkinter.CTkButton(self, text="Delete All Data", command=self.buttonDAData_callback)
        self.buttonSData.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.buttonExit = customtkinter.CTkButton(self, text="Exit", command=self.buttonExit_callback)
        self.buttonExit.grid(row=9, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    def buttonGData_callback(self):
        print("Change Global Data pressed")
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        cWeight = data[0]["globalWeight"]
        gCalorie = data[0]["gloabalCalories"]
        diet = data[0]["diet"]
        whatchange = simpledialog.askstring("Input","What do you wanna change(Weight[w]/Calorie[c]/Diet[d])")
        if whatchange == "w":
            cWeight = simpledialog.askfloat("Input", "What is your current weight in kg:")
            if cWeight <= 0:
                self.errorWithData("Weight can't be 0 or less!")
        elif whatchange == "c":
            gCalorie = simpledialog.askinteger("Input", "What is your daily calorie intake in kcal:")
            if gCalorie <= 0:
                self.errorWithData("Calorie Intake can't be 0 or less!")
        elif whatchange == "d":
            diet = simpledialog.askstring("Input", "What is your diet? (Bulking[b]/Cutting[c]/Maintenance[m]):")
            if diet.lower() == "b":
                diet = "Bulking"
            elif diet.lower() == "c":
                diet = "Cutting"
            elif diet.lower() == "m":
                diet = "Maintenance"
            else:
                self.errorWithData("Please enter a valid diet (Bulking[b]/Cutting[c]/Maintenance[m])")
        else:
            self.errorWithData("Please enter a valid input (Weight[w]/Calorie[c]/Diet[d])")
        data2 = {0:{"globalWeight": cWeight, "gloabalCalories": gCalorie, "diet": diet}}
        data3 = {**data, **data2}
        with open(file_path, 'wb') as f:
            pickle.dump(data3, f) 
        print("Your Data was changed successfully!")
        showDataFile(self)
        return 0
    
    def buttonDData_callback(self):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        currentDay = 0
        for i in data:
            currentDay = i
        currentDay = currentDay + 1
        print("Your current day is: " + str(currentDay)) 
        currentWeight = simpledialog.askfloat("Input", "Your current day is: " + str(currentDay) + ". What is your weight today in kg: ")
        currentCalories = simpledialog.askinteger("Input","What is your calorie intake today in kcal: ")
        if currentCalories <= 0 or currentWeight <= 0:
            self.errorWithData("Weight or Calorie Intake can't be 0 or less!")
        train = simpledialog.askstring("Input","Did you do any Training today? (yes/no): ")
        if train == "yes":
            todaysTraining = simpledialog.askinteger("Input","How many Calories did you burn today in Training in kcal: ")
            if todaysTraining <= 0:
                self.errorWithData("You can't burn 0 or less Calories!")
        else:
            todaysTraining = 0
        totalCalories = int(currentCalories) - int(todaysTraining)
        data2 = {currentDay:{"currentWeight": float(currentWeight), "totalCalories": totalCalories}}
        data3 = {**data, **data2}
        with open(file_path, 'wb') as af:
            pickle.dump(data3, af)
        print("Your Data was added successfully!")
        showDataFile(self)
        return 0
    
    def buttonCDData_callback(self):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        currentDay = 0
        for i in data:
            currentDay = i
        currentDay = currentDay
        messagebox.showinfo("Information","Your current day is: " + str(currentDay))
        whichDay = simpledialog.askinteger("Input","Which day do you want to change: ")
        whichDay = int(whichDay)
        if whichDay not in data:
            messagebox.showinfo("Information","This day does not exist yet. Please add the day first.")
            exit()
        elif whichDay == 0:
            messagebox.showinfo("Information","You can't change the startweight and the startcalories. Please change the global data instead.")
        else:
            whatChange = simpledialog.askstring("Input","What do you want to change? (Weight[w]/Calories[c]/TrainingCalories[t]/exit[e]): ")
            if whatChange == "w":
                currentWeight = simpledialog.askfloat("Input","What is your weight today in kg: ")
                if currentWeight <= 0:
                    self.errorWithData("Weight can't be 0 or less!")
                data[whichDay]["currentWeight"] = float(currentWeight)
            elif whatChange == "c":
                changeWhat = simpledialog.askstring("Input","Do you wanna add, subtract or change the total calories? (add[a]/sub[b]/change[c]): ")
                if changeWhat == "a":
                    currentCalories = simpledialog.askinteger("Input","How manny Calories you wanna add: ")
                    if currentCalories <= 0:
                        self.errorWithData("You can't add 0 or less Calories!")
                    data[whichDay]["totalCalories"] = int(data[whichDay]["totalCalories"]) + int(currentCalories)
                elif changeWhat == "b":
                    currentCalories = simpledialog.askinteger("Input","How manny Calories you wanna subtract: ")
                    if currentCalories <= 0 or currentCalories > int(data[whichDay]["totalCalories"]):
                        self.errorWithData("You can't subtract 0 or less Calories or more then your total intake!")
                    data[whichDay]["totalCalories"] = int(data[whichDay]["totalCalories"]) - int(currentCalories)
                elif changeWhat == "c":
                    currentCalories = simpledialog.askinteger("Input","What is your calorie intake today in kcal: ")
                    todaysTraining = simpledialog.askinteger("Input","How many Calories did you burn today in Training in kcal: ")
                    if currentCalories <= 0 or todaysTraining <= 0:
                        self.errorWithData("Weight or Calorie Intake can't be 0 or less!")
                    totalCalories = int(currentCalories) - int(todaysTraining)
                    data[whichDay]["totalCalories"] = int(totalCalories)
                else:
                    self.errorWithData("Please enter a valid input (add[a]/sub[b]/change[c])")
            elif whatChange == "t":
                changeWhat = input("Do you wanna add or subtract the training calories? (add[a]/sub[b]): ")
                if changeWhat == "a":
                    todaysTraining = simpledialog.askinteger("Input","How manny Calories did you burn: ")
                    if todaysTraining <= 0:
                        self.errorWithData("You can't burn 0 or less Calories!")
                    data[whichDay]["totalCalories"] = int(data[whichDay]["totalCalories"]) - int(todaysTraining)
                    print("You Data was changed successfully!")
                elif changeWhat == "b":
                    todaysTraining = simpledialog.askinteger("Input","How manny Calories you wanna subtract from Training: ")
                    if todaysTraining <= 0 or todaysTraining > int(data[whichDay]["totalCalories"]):
                        self.errorWithData("You can't subtract 0 or less Calories or more then your total intake!")
                    data[whichDay]["totalCalories"] = int(data[whichDay]["totalCalories"]) + int(todaysTraining)
                    print("You Data was changed successfully!")
            elif whatChange == "e":
                exit()
            else:
                exit()
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        print("You Data was changed successfully!")
        showDataFile(self)
        return 0
    
    def buttonDDData_callback(self):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        currentDay = 0
        for i in data:
            currentDay = i
        currentDay = currentDay
        messagebox.showinfo("Information","Your current day is: " + str(currentDay))
        whichDay = simpledialog.askinteger("Input","Which day do you want to delete: ")
        whichDay = int(whichDay)
        if whichDay not in data:
            messagebox.showinfo("Information","This day does not exist yet. Please add the day first.")
            exit()
        elif whichDay == 0:
            messagebox.showinfo("Information","You can't delete the startweight and the startcalories. Please change the global data instead.")
            exit()
        else:
            delete = simpledialog.askstring("Input","Do you really wanna delete this day? (yes/no): ")
            if delete == "yes":
                del data[whichDay]
                messagebox.showinfo("Information","Your Data was deleted successfully!")
            elif delete == "no":
                messagebox.showinfo("Information","Your Data was not deleted!")
            else:
                exit()
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        showDataFile(self)
        return 0
    
    def buttonSData_callback(self):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        whichDay = simpledialog.askinteger("Input","Which day do you want to show: ")
        whichDay = int(whichDay)
        if whichDay not in data:
            messagebox.showinfo("Information","This day does not exist yet. Please add the day first.")
        else:
            messagebox.showinfo("Information","Weight: " +str(data[whichDay]["currentWeight"]) + " kg, Calorie: " + str(data[whichDay]["totalCalories"]) + " kcal")
        showDataFile(self) 
        return 0
    
    def buttonDAData_callback(self):
        delete = simpledialog.askstring("Input","Do you really wanna delete all data? (yes/no): ")
        if delete == "yes":
            os.remove("data.pkl")
            messagebox.showinfo("Information","All Data was deleted successfully!")
        elif delete == "no":
            messagebox.showinfo("Information","Your Data was not deleted!")
        exit()
    
    def errorWithData(self, msg):
        messagebox.showinfo("Error", msg)
        exit()

    def buttonExit_callback(self):
        exit()


def createDataFile(app):
    # Check if the file exists
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        # If the file does not exist, create an empty pickle file
        info = app.createData()
        if info[0] == None or info[1] == None or info[2] == None:
            exit()
        Day = 0
        if info[2].lower() == "b":
            info[2] = "Bulking"
        elif info[2].lower() == "c":
            info[2] = "Cutting"
        elif info[2].lower() == "m":
            info[2] = "Maintenance"
        else:
            app.errorWithData()
        if info[0] <= 0 or info[1] <= 0:
            app.errorWithData("Weight or Calorie Intake can't be 0 or less!")
        data = {Day:{"globalWeight": info[0], "gloabalCalories": info[1], "diet": info[2]}}
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        print("Your Data was created successfully!")

def showDataFile(app):
    # Load the data from the file
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    currentDay = 0
    for i in data:
        currentDay = i
    # Print the data
    if currentDay == 0:
        app.showDataFile1(currentDay, str(data[0]["globalWeight"]), str(data[0]["gloabalCalories"]), str(data[0]["diet"]), 0, 0, 0, 0)
    else:
        analyst = dataAnalysis()
        weeklyweightDif = weeklyWeightDif()
        app.showDataFile1(currentDay, str(data[0]["globalWeight"]), str(data[0]["gloabalCalories"]), str(data[0]["diet"]), str(data[currentDay]["currentWeight"]), str(data[currentDay]["totalCalories"]), analyst, weeklyweightDif)

def dataAnalysis():
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    currentDay = 0
    for i in data:
        currentDay = i
    if data[0]["diet"] == "Bulking":
        if data[currentDay]["totalCalories"] > int(data[0]["gloabalCalories"] + 500):
            return "Even when you are Bulking, you should not eat t0o much."
        elif data[currentDay]["totalCalories"] <= int(data[0]["gloabalCalories"]):
            return "You are eating to less. You should eat more!"
        elif data[currentDay]["totalCalories"] + 200 > int(data[0]["gloabalCalories"]) and data[currentDay]["totalCalories"] <= int(data[0]["gloabalCalories"] + 500):
            return "You are eating enough. Keep going!"
        else:
            return "You should eat at least 200 kcal more then your daily intake!"
    elif data[0]["diet"] == "Cutting":
        if data[currentDay]["totalCalories"] > int(data[0]["gloabalCalories"]):
            return "You are eating to much. You should eat less!"
        elif data[currentDay]["totalCalories"] <= int(data[0]["gloabalCalories"] - 700):
            return "You are eating to less. You should eat more!"
        elif data[currentDay]["totalCalories"] > int(data[0]["gloabalCalories"] - 700) and data[currentDay]["totalCalories"] <= int(data[0]["gloabalCalories"]) - 200:
            return "You are perfectly cutting. Keep going!"
        else:
            return "You should eat at least 200 kcal less then your daily intake!"
    elif data[0]["diet"] == "Maintenance":
        if data[currentDay]["totalCalories"] < int(data[0]["gloabalCalories"] + 200 or data[currentDay]["totalCalories"] > int(data[0]["gloabalCalories"] - 200)):
            return "You are perftectly eating. Keep going!"
        elif data[currentDay]["totalCalories"] > int(data[0]["gloabalCalories"] + 200):
            return "You are eating to much. You should eat less!"
        else:
            return "You are eating to less. You should eat more!"
        
def weeklyWeightDif():
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    daysrecorded = 0
    for i in data:
        daysrecorded = i
    if daysrecorded < 8:
        return "No Weekly Data yet"
    else:
        weeklyWeightDif = float(data[daysrecorded]["currentWeight"]) - float(data[daysrecorded -7]["currentWeight"]) 
        return str(round(weeklyWeightDif, 2)) + " kg"

app = App()
createDataFile(app)
showDataFile(app)
app.showbutton()
app.mainloop()

