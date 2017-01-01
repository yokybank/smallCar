filename=open('carData12.11.2.txt','a+')
#file2=open('2.txt','a+')
fileArray=filename.readlines()
for i in fileArray:
    filename.write(i)
filename.close()
#file2.close()