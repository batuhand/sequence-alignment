inputfile ="nCovid.txt"
f = open(inputfile, "r") 
seq = f.read() 
   
seq = seq.replace("\n", "")  
seq = seq.replace("\r", "") 

stops = ["TTA","TGA","TAG"]    
lst1 = [] 
lst2 = [] 
start = 0 
counter = 0 
for i in range (3):
    lst1.append([])
    lst2.append([])

while (seq and counter < 3):

    for i in range(start,len(seq),3):
        codon = seq[i:i+3] 
        
        if(codon == "ATG"): 
            lst1[start].append(i+1) 

        if(codon in stops): 
            lst2[start].append(i+1) 


    start += 1 
    counter += 1 

lst1str = ' '.join(map(str, lst1))
lst2str = ' '.join(map(str, lst2))

result_file = open("nCovid_ORF.txt", "w")
result_file.write("Start Codonlar\n")
result_file.write(lst1str)
result_file.write("\nStop Codonlar\n")
result_file.write(lst2str)
result_file.close()

print("Start Codonlar")
print(lst1)
print("Stop Codonlar")
print(lst2)