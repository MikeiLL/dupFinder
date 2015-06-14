# dupFinder
Find and potentially delete duplicate files between multiple directories, even if they have different names but the same content.

Install by cloning this repository:

`git clone git@github.com:MikeiLL/dupFinder.git`

`cd dupFinder` into the directory.

Now test the program with `python dupFinder.py -t path_to_directory/` or 
`python dupFinder.py -t path_to_directory/ path_to_another_directory/, etc...`

To get "path" to directories you can get into the directory and type `pwd`, which means `print working directory`.

This will be all be done through a 'terminal' - on OSX it's in Applications-> Utilities-> Terminal.

To actually REMOVE the duplicate files run the program as above but without the `-t` test flag.

Removed files will be backed up to a new directory named `removed`_ the current time.
