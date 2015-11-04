
 
import os, glob	#Importing necessary headfiles
import Image
import hashlib
import shutil
import imagehash

hashdict={}	#defining hashdictionary globally so that it is easily accessible
    
def image_hash(imagefile):	#function to return the md5 hash value for an image present in the 'imagefile' location
    img = Image.open(imagefile)
    return hashlib.md5(img.tostring()).hexdigest()
 
def findduplicates(dataset_path):	#function to find the exact duplicates of an image, returns the duplicates list as well as the hashdict - unique image files
    duplicatelist=[]
    for imgfile in glob.glob(dataset_path + os.sep +"*.jpg"):
        filen, ext = os.path.splitext(imgfile)
        fileid = filen.split(os.sep)
        filehash = image_hash(imgfile)
        if hashdict.has_key(filehash):
            duplicatelist.append(fileid)
        else:
            hashdict[filehash]=fileid
    return duplicatelist, hashdict

def findnearduplicates(dataset_path):	#function to find near duplicates - uses perceptual hash from the imagehash module, returns both the duplicates list as well as the hashdict
    duplicatelist=[]
    for imgfile in glob.glob(dataset_path + os.sep +"*.jpg"):
        filen, ext = os.path.splitext(imgfile)
        fileid = filen.split(os.sep)
        img = Image.open(imgfile)
        filehash = str(imagehash.dhash(img))
        if hashdict.has_key(filehash):
            duplicatelist.append(fileid)
        else:
            hashdict[filehash]=fileid
    return duplicatelist, hashdict

def writeduplicates(dataset_path,duplicatelist):	#function to copy all the duplicate files into a separate folder and write down their original locations in file
    destin_path = raw_input('Enter the destination path for duplicate images- no quotes, no ending slash: ')
    f = open('duplicate_file_list.txt','ab')
    for imgfileid in duplicatelist:
        if os.path.isfile(os.path.join(dataset_path+os.sep, imgfileid[-1] + '.jpg')):
            f.write(dataset_path + os.sep + imgfileid[-1] + '.jpg')
            f.write('\n')
            shutil.copy(os.path.join(dataset_path+os.sep, imgfileid[-1] + '.jpg') , os.path.join(destin_path, imgfileid[-1] + '.jpg'))
    f.close()

def writefinal(dataset_path,hashdict):	#function to copy all the unique images from the dataset into a separate folder and write down their original locations in file
    destin_path = raw_input('Enter the destination path for final images- no quotes, no ending slash: ')
    f = open('final_image_files_list.txt','ab')
    for key,value in hashdict.iteritems():
        if os.path.isfile(os.path.join(dataset_path, value[-1] + '.jpg')):
            f.write(dataset_path + os.sep + value[-1] + '.jpg')
            f.write('\n')
            shutil.copy(os.path.join(dataset_path, value[-1] + '.jpg') , os.path.join(destin_path, value[-1] + '.jpg'))
    f.close()

def main():	#main function takes input whether to find exact or near duplicates, can continuously keep adding images as new datasets are given
	dataset_path = raw_input('Enter the dataset path- no quotes, no ending slash: ')
	in1 = input('Do you want to find exact duplicates or nearduplicates(1 or 2): ')
	if in1 == 1:
		duplicatelist, hashdict = findduplicates(dataset_path)
		print("Duplicate Data obtained")
		writeduplicates(dataset_path,duplicatelist)
		print("Duplicate image files written")
		writefinal(dataset_path,hashdict)
		print("Final image files written")
		a = raw_input('Do you want to add further images (y or n): ')
		while (a == 'y'):
			dataset_path = raw_input('Enter the dataset path- no quotes, no ending slash: ')
			duplicatelist, hashdict = findduplicates(dataset_path)
			print("Duplicate Data obtained")
			writeduplicates(dataset_path,duplicatelist)
			print("Duplicate image files written")
			writefinal(dataset_path,hashdict)
			print("Final image files written")
			a = raw_input('Do you still want to add further images (y or n): ')
		print("Done")
	if in1 == 2:
		duplicatelist, hashdict = findnearduplicates(dataset_path)
		print("Near Duplicate Data obtained")
		writeduplicates(dataset_path,duplicatelist)
		print("Near Duplicate image files written")
		writefinal(dataset_path,hashdict)
		print("Final image files written")
		a = raw_input('Do you want to add further images (y or n): ')
		while (a == 'y'):
			dataset_path = raw_input('Enter the dataset path- no quotes, no ending slash: ')
			duplicatelist, hashdict = findduplicates(dataset_path)
			print("Duplicate Data obtained")
			writeduplicates(dataset_path,duplicatelist)
			print("Duplicate image files written")
			writefinal(dataset_path,hashdict)
			print("Final image files written")
			a = raw_input('Do you still want to add further images (y or n): ')
		print("Done")

		
if __name__ == "__main__": main()
