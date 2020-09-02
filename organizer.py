import os
import datetime
import shutil

def user_input(inp):
    '''
    Use input or raw_input depending 
    on python version (for python 2 
    compatibility)
    '''
    try:
        return raw_input(inp)
    except NameError:
        return input(inp)

def get_inputs():
    '''
    Get source and destination filepaths, confirming at each stage that the 
    filepaths are valid and that the source filepath contains the expected number of 
    photo files.
    '''
    # define searched file types
    EXTS = ('.tif', '.jpg', '.png', '.jpeg')

    while True:    
        # directory where photos are located
        source = user_input("Path to photos: ")
        # replace above with below for python2 compatibility
        # source = raw_input("Path to photos: ")

        # check valid dir
        if not os.path.exists(source):
            print('Filepath provided is not valid. Please enter again.')
            continue

        # report number of photos in directory and confirm
        fnames = []    
        for dirpath, _, files in os.walk(source):
            for filename in files: 
                fname = os.path.join(dirpath,filename) 
                if fname.endswith(EXTS): 
                    fnames.append(fname)
        
        # (used format for python2 compatibility)
        confirm = user_input('Found {} picture files in directory. \nContinue (Y/N)?: '.format(len(fnames)))

        if confirm.lower() in ['n', 'no']:
            continue

        # directory where photos will be copied into new folders
        dest = user_input('Path for organized photos:')
        # replace above with below for python2 compatibility
        # dest = raw_input("Path for organized photos: ")

        if not os.path.exists(dest):
            print('Filepath provided is not valid. Please start again.')
            continue

        else:
            break
           
    return fnames, dest

def organizer(fnames, dest):
    '''
    Copies a list of files to a given directory,
    organizing them into folders by the month and year
    of their creation date.
    '''

    if len(fnames) == 0:
        return ValueError
    if not os.path.exists(dest):
        return ValueError

    print('Organizing and copying {} files to: \n{}'.format(len(fnames), dest))
    
    dirs_created = 0
    files_copied = 0
    failed = 0
    def get_month_dir(fname):
        '''
        Helper function that creates a new folder path based on 
        the provided destination directory and the 
        as 'Month YYYY' e.g. 'September 2016'.
        '''
        
        dt = datetime.datetime.fromtimestamp(
            os.stat(fname).st_birthtime
        ).strftime('%B %Y')

        newloc = '/'.join([dest, dt])

        return newloc
 
    for fname in fnames:
        # get new dirname for file
        try:
            dirname = get_month_dir(fname)
        except:
            print('Could not access file creation date.')
            failed += 1
            continue

        # create dir if needed
        if not os.path.exists(dirname):
            try:    
                os.mkdir(dirname)
                dirs_created += 1
            except:
                print('Failed to create {}'.format(dirname))
                failed += 1
                continue

        # join dirname with file name for new path
        newpath = '/'.join([dirname, os.path.split(fname)[1]])
        
        # copy to new location
        if not os.path.exists(newpath):
            try:
                shutil.copyfile(fname, newpath)
                files_copied += 1
            except:
                print('Failed to copy {} to {}'.format(fname, newpath))
                failed += 1
                continue

    print('Created {} new folders and copied {} files.'.format(dirs_created, files_copied))

if __name__ == "__main__":
    
    # get source files to copy and destination
    fnames, dest = get_inputs()
    
    # copy to folders in new dir by month
    organizer(fnames, dest)
