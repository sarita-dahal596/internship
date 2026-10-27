f = open("file handlingg.py","r")
data = f.read()
print(data)
print(type(data))
f.close()

#upto
f = open("file handlingg.py","r")
data = f.read(6) #file ko 6 samma ko dinxa out-> f = op
print(data)
print(type(data))
f.close()

#line
f = open("file handlingg.py","r")
line1 = f.readline()
print(line1)

line2 = f.readline()
print(line2)
f.close()

#write
f = open("file handlingg.py","w")
f.write("\n")

f = open("file handlingg.py","r+")
f.write("abc")
print(f.read())
f.close()

f = open("demo.txt","w")
data = f.read()
print(data)
print(type(data))
f.close()
f = open("demo.txt","w")