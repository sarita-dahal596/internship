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



print("ENTER PATENT1 DETAILS")
name = input("Enter name: ")
age = int(input("Enter age: "))
disease = input("Enter disease: ")
bill = float(input("Enter bill: "))

p1 = Patient(name, age, disease, bill) #creating object

print("ENTER PATENT2 DETAILS")
name = input("Enter name: ")
age = int(input("Enter age: "))
disease = input("Enter disease: ")
bill = float(input("Enter bill: "))

p2 = Patient(name,age,disease,bill)
p1.display()
p2.display()




