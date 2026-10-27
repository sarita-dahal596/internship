#read file
f = open("demo.txt", "r")
data = f.read()
print(data)
print(type(data))
f.close()

#2samma dinxa
f = open("demo.txt", "r")
data = f.read(2)
print(data)
print(type(data))
f.close()

#line
f = open("demo.txt", "r")
line1 = f.readline()  #first line ko data dinxa
print(line1)

line2 = f.readline()
print(line2 )

#write
f = open("demo.txt", "w")
f.write("i want to write here")  #in demo.txt ma yo write hunchha agadiko janxa
f.close()

#apend
f = open("demo.txt", "a")
f.write("\nand i want to eat")  #in demo.txt ma yo add hunchha
f.close()

#r+ first ma overwrite
f = open("demo.txt", "r+")
f.write("don't want ")
f.close()

#first ma overwrite garara dont't want dekhi print hunchha
f = open("demo.txt", "r+")
f.write("don't want ")
print(f.read())  # ja pointer aauxa thye bata read garxa
f.close()

#w+
f = open("demo.txt", "w+")
print(f.read())  #print nothing trunated
f.write("i am eating")
f.close()

#a+append
f = open("demo.txt", "a+")
print(f.read())
f.write("i am dancing")
f.close()


with open("demo.txt", "r") as f:
     data = f.read()
new_data = data.replace("eating","singing")
print(new_data)

with open("demo.txt", "r") as f:
     f.write(new_data)








