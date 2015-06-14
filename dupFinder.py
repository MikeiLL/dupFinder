# dupFinder.py
import os, sys, shutil, datetime
import hashlib
 
def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            print(path)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups
 
 
# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
 
 
def hashfile(path, blocksize = 65536):
	print(path)
	afile = open(path, 'rb')
	hasher = hashlib.md5()
	buf = afile.read(blocksize)
	while len(buf) > 0:
		hasher.update(buf)
		buf = afile.read(blocksize)
	afile.close()
	return hasher.hexdigest()
 
 
def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if not 'testrun' in globals():
    	backupdir = 'removed_' + str(datetime.datetime.now())
    	if not os.path.exists(backupdir):
    		os.makedirs(backupdir)
    else:
	backupdir = 'backup_fir_date_now'
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('^^^^^^^^^^^^^^^^^')
        count = 0
        for result in results:
            for subresult in result:
                if count == 0:
			print('KEEPING ONE COPY: %s.' % subresult)
			count += 1
		elif 'testrun' in globals():
			print('\t\t %s WILL BE REMOVED TO: %s' % (subresult, backupdir))
		else:
                	print('\t\tREMOVING %s TO %s' % (subresult, backupdir))
			try:
				shutil.move(subresult, backupdir)
			except shutil.Error:
				print ('\t\t EXISTS. DELETING.')
				os.remove(subresult)
            print('___________________')
 
    else:
        print('No duplicate files found.')
 
 
if __name__ == '__main__':
    if len(sys.argv) > 1:
        dups = {}
	if sys.argv[1] == '-t':
		testrun = 1
        	folders = sys.argv[2:]
	else: folders = sys.argv[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDicts(dups, findDup(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        printResults(dups)
    else:
        print('Usage: python dupFinder.py [-t] folder or python [-t] dupFinder.py folder1 folder2 folder3')
