# dupFinder.py
import os
import sys
from shutil import move
from datetime import datetime
from hashlib import md5

usage = 'Usage: python dupFinder.py [-t] folder or python [-t] dupFinder.py folder1 folder2 folder3'

def find_duplicates(parentFolder):
    """ 
    Build and return an object with a key for each unique hash, and a 
    list of all matching files as it's value: {hash:[names]}
    """
    dups = {}
    for dir_name, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dir_name)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dir_name, filename)
            print(path)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups
 
 
def join_dicts(dict1, dict2):
    """
    
    """
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
 
 
def hashfile(path, blocksize = 65536):
    """
    Build and return hash by reading file in blocks and updating the md5 instance.
    """
    print(path)
    afile = open(path, 'rb')
    hasher = md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 
 
def handle_results(dict1, testrun=0):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if not testrun:
    	backupdir = 'removed_' + str(datetime.now())
    	if not os.path.exists(backupdir):
    		os.makedirs(backupdir)
    else:
	    backupdir = 'backup_dir_date_now'
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
                if testrun:
                    print('\t\t %s WILL BE REMOVED TO: %s' % (subresult, backupdir))
                else:
                    print('\t\tREMOVING %s TO %s' % (subresult, backupdir))
                    try:
                        move(subresult, backupdir)
                    except shutil.Error:
                        print ('\t\t EXISTS. DELETING.')
                        os.remove(subresult)
                    print('___________________')
    else:
        print('No duplicate files found.')
 
def main(args): 
    if len(args) > 1:
        dups = {}
	if args[1] == '-t':
		testrun = 1
        	folders = args[2:]
	else: folders = args[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                join_dicts(dups, find_duplicates(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        handle_results(dups, testrun)
    else:
        print(usage)

if __name__ == '__main__':
    main(sys.argv)

