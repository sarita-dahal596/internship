class Patient:
    hospital_name = "City Care Hospital" #class variable
    total_patients = 0 #keeps track of how many patient objects have been created.

    def __init__(self, name, age, disease, bill):
        self.name = name  #instance variable
        self.age = age
        self.disease = disease
        self.bill = bill

        Patient.total_patients += 1  #increases the class variable every time a new patient is created.

    @staticmethod    #this method doesn't need self.
    def hospital_info():
        print("Hospital:", Patient.hospital_name)
        print("Emergency: 24 hours")

    def display(self):
        print("Name:", self.name)  #self becz it need info of  particular patient
        print("Age:", self.age)
        print("Disease:", self.disease)
        print("Bill:", self.bill)





# Creating objects
p1 = Patient("James", 25, "Fever", 20000)
p2 = Patient("John", 40, "Diabetes", 60000)

# Display patient information
p1.display()
print()

p2.display()
print()




# Class variable
print("Total patients:", Patient.total_patients)



# Static method
Patient.hospital_info()