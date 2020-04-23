import xlsxwriter

arr1 = []
skinmm= []
skinc= []
liverc= []
with open("CosmicMutantExportCensus.tsv","r",encoding="utf-8") as file: 
    arr1 = file.readlines()                                                 # Dosya okunup listeye atıldı

workbook = xlsxwriter.Workbook('Odev2.xlsx')
patientsAndGenesSheet = workbook.add_worksheet('Hastalar ve Genler')        

patientsAndGenesSheet.write(0, 0, 'Skin-Malignant_melanoma')
patientsAndGenesSheet.write(0, 2, 'Skin-carcinoma')
patientsAndGenesSheet.write(0, 4, 'Liver-carcinoma')                        # Excel dosyası oluşturuldu

a = 1
b = 1
c = 1

for i in arr1:
    kayit = i.split("\t")
    if kayit[7] == "skin" and kayit[11] == "malignant_melanoma":            # Skin Malignant_melanoma hastalığına sahip olan hasta id'leri ve
        patientsAndGenesSheet.write(a, 0, str(kayit[5]))                    # Genler Excel dosyasına yazıldı
        patientsAndGenesSheet.write(a, 1, str(kayit[0]))    
        a += 1
        skinmm.append(kayit)
    elif kayit[7] == "skin" and kayit[11] == "carcinoma":                   # Skin Carcinoma hastalığına sahip olan hasta id'leri ve
        patientsAndGenesSheet.write(b, 2, str(kayit[5]))                    # Genler Excel dosyasına yazıldı
        patientsAndGenesSheet.write(b, 3, str(kayit[0]))
        b += 1
        skinc.append(kayit)
    elif kayit[7] == "liver" and kayit[11] == "carcinoma":                  # Liver Carcinoma hastalığına sahip olan hasta id'leri ve
        patientsAndGenesSheet.write(c, 4, str(kayit[5]))                    # Genler Excel dosyasına yazıldı
        patientsAndGenesSheet.write(c, 5, str(kayit[0]))
        c += 1
        liverc.append(kayit)

def createDict (arr):                                                       # Bu fonksiyon verilen listedeki genlerin her birinin 
                                                                            # Toplam bulunma sayısını anahtar değer şekilde sözlüğe kaydeder
    dct = {}

    for j in arr:
        if j[0] in dct.keys():
            dct[j[0]] +=1
        else:
            dct[j[0]] = 1

    return dct

skinmm_Dict = createDict(skinmm)
skinc_Dict = createDict(skinc)
liverc_Dict = createDict(liverc)

def getTop30gene (dct, arr2):                                               # Bu fonksiyon verilen sözlükteki en çok bulunan 30 geni ve yüzdelerini bir listeye kaydeder

    arr = []

    listofTuples = sorted(dct.items(), reverse=True, key=lambda x: x[1])

    # Iterate over the sorted sequence
    for elem in range(0,30):

        arr1 = []
        arr1.append(listofTuples[elem][0])
        arr1.append(listofTuples[elem][1])
        arr1.append(int(listofTuples[elem][1])/len(arr2)*100)
        arr.append(arr1)

    return arr

skinmm_top30 = getTop30gene(skinmm_Dict, skinmm)
skinmc_top30 = getTop30gene(skinc_Dict, skinc)
liverc_top30 = getTop30gene(liverc_Dict, liverc)

def writeToXLSX (arr, fileName, startColumn):                                # Bu fonksiyon verilen listeyi uygun biçimde excel dosyasına yazar

    x = 1

    for b in arr:

        top30gene.write(x, startColumn, str(b[0]))
        top30gene.write(x, startColumn + 1, str(b[1]))
        top30gene.write(x, startColumn + 2, str(b[2]))
        x += 1

top30gene = workbook.add_worksheet('Top 30 gene')
top30gene.write(0, 0, 'Skin-Malignant_melanoma')
top30gene.write(0, 3, 'Skin-carcinoma')
top30gene.write(0, 6, 'Liver-carcinoma')

writeToXLSX(skinmm_top30, "skin-malignant_melanoma-top30gene.txt",0)
writeToXLSX(skinmc_top30, "skin-carcinoma-top30gene.txt", 3)
writeToXLSX(liverc_top30, "liver-carcinoma-top30gene.txt", 6)

skinCompLiver = []

for gene in skinc_Dict.keys():                                              # Farklı iki sözlükteki genlerin aynı olup olmadığı ve bulunma benzerlikleri
                                                                            # karşılaştırıldı
    if gene in liverc_Dict.keys():

        arr = []
        arr.append(gene)
        percentageSkinc = skinc_Dict[gene]/len(skinc)*100
        arr.append(percentageSkinc)
        percentageLiverc = liverc_Dict[gene]/len(liverc)*100
        arr.append(percentageLiverc)
        if percentageSkinc > percentageLiverc:
            arr.append(percentageLiverc/percentageSkinc*100)
        else:
            arr.append(percentageSkinc/percentageLiverc*100)

        skinCompLiver.append(arr)

skinCompLiver.sort(key=lambda x: x[3], reverse=True)

skinCompLiverSheet = workbook.add_worksheet('skin-c_liver-c_Comparing')

skinCompLiverSheet.write(0, 0, 'Gene Name')
skinCompLiverSheet.write(0, 1, 'SkinC%')
skinCompLiverSheet.write(0, 2, 'LiverC%')
skinCompLiverSheet.write(0, 3, 'Similarity')

y = 1

for b in skinCompLiver:

    skinCompLiverSheet.write(y, 0, str(b[0]))
    skinCompLiverSheet.write(y, 1, str(b[1]))
    skinCompLiverSheet.write(y, 2, str(b[2]))
    skinCompLiverSheet.write(y, 3, str(b[3]))

    y += 1

tripleComp = []

for gene in skinc_Dict.keys():                                              # Farklı üç sözlükteki genlerin aynı olup olmadığı ve bulunma benzerlikleri
                                                                            # karşılaştırıldı
    if gene in liverc_Dict.keys() and gene in skinmm_Dict.keys():

        arr = []
        arr.append(gene)
        percentageSkinc = skinc_Dict[gene]/len(skinc)*100
        arr.append(percentageSkinc)
        percentageLiverc = liverc_Dict[gene]/len(liverc)*100
        arr.append(percentageLiverc)
        percentageSkinMM = skinmm_Dict[gene]/len(skinmm)*100
        arr.append(percentageSkinMM)

        if percentageSkinc > percentageLiverc:
            pcSkinCLiverC = percentageLiverc/percentageSkinc*100
        else:
            pcSkinCLiverC = percentageSkinc/percentageLiverc*100

        if percentageSkinc > percentageSkinMM:
            pcSkinCSkinMM = percentageSkinMM/percentageSkinc*100
        else:
            pcSkinCSkinMM = percentageSkinc/percentageSkinMM*100

        if percentageSkinMM > percentageLiverc:
            pcSkinMMLiverC = percentageLiverc/percentageSkinMM*100
        else:
            pcSkinMMLiverC = percentageSkinMM/percentageLiverc*100

        arr.append((pcSkinCLiverC + pcSkinCSkinMM + pcSkinMMLiverC) / 3)

        tripleComp.append(arr)

tripleComp.sort(key=lambda x: x[4], reverse=True)

tripleCompSheet = workbook.add_worksheet('TripleComparing')

tripleCompSheet.write(0, 0, 'Gene Name')
tripleCompSheet.write(0, 1, 'SkinC%')
tripleCompSheet.write(0, 2, 'LiverC%')
tripleCompSheet.write(0, 3, 'SkinMM%')
tripleCompSheet.write(0, 4, 'Similarity')

z = 1

for b in tripleComp:

    tripleCompSheet.write(z, 0, str(b[0]))
    tripleCompSheet.write(z, 1, str(b[1]))
    tripleCompSheet.write(z, 2, str(b[2]))
    tripleCompSheet.write(z, 3, str(b[3]))
    tripleCompSheet.write(z, 4, str(b[4]))

    z += 1

workbook.close()
        

            


