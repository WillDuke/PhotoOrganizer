# org_gui.py
import os
import datetime
import shutil
import PySimpleGUI as sg

# camera icon
#Icons made by <a href="https://www.flaticon.com/authors/google" title="Google">Google</a> 
# from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

# ----- Full layout -----
column_1 = [
    [
        sg.Text("Source", size = (8, 1), justification= 'center'),
        sg.In(size=(25, 1), enable_events=True, key="-SOURCE-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Destination", size = (8, 1), justification= 'center'),
        sg.In(size=(25, 1), enable_events=True, key="-DEST-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Output(size=(41,8))
    ],
    [
        sg.Button('Organize', size = (25, 1), pad = ((0, 0), (3, 0)))
    ]
]

column_2 = [[sg.Listbox(
            values=[], size=(45, 13), key="-FILE LIST-", pad = ((3,0), (0, 3))
        )],
        [sg.ProgressBar(100, orientation='h', size=(32, 20), key='progbar')]
        ]

layout = [[
        sg.Column(column_1, element_justification= 'c'),
        sg.VSeperator(),
        sg.Column(column_2)
]]

window = sg.Window("Photo Organizer", layout, element_justification='c')


def organizer(fnames, dest, window):
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

        newloc = os.path.join(dest, dt)

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
        base = os.path.basename(fname)
        newpath = os.path.join(dirname, base)
        
        # copy to new location
        try:
            if not os.path.exists(newpath):
                shutil.copyfile(fname, newpath)
            else:
                np_wo_ext, ext = os.path.splitext(newpath)
                shutil.copyfile(fname, np_wo_ext + '_copy' + ext)
            files_copied += 1
        except:
            print('Failed to copy {} to {}'.format(fname, newpath))
            failed += 1
            continue
            
        # update the progress bar
        try:
            window['progbar'].update_bar(files_copied + 1, max = len(fnames))
        except:
            print('Progress update failed.')
            continue

    print('Created {} new folders and copied {} files.'.format(dirs_created, files_copied))
    print('Failed to copy {} files.'.format(failed))

# Run the Event Loop
while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-SOURCE-":
        folder = values["-SOURCE-"]

        EXTS = ('.tif', '.jpg', '.png', '.jpeg')
        pathnames = []
        fnames = [] 

        try:
            for dirpath, _, files in os.walk(folder):
                for filename in files: 
                    pathname = os.path.join(dirpath,filename) 
                    if pathname.endswith(EXTS): 
                        pathnames.append(pathname)
                        fnames.append(filename)
            if len(folder) != 0:
                print("Found {} image files to copy.".format(len(fnames)))

        except:
            print('Photo search failed. Please try a different source folder.')

        window["-FILE LIST-"].update(fnames)

    if event == 'Organize':
        try:
            organizer(pathnames, values["-DEST-"], window)
        except:
            print('Please provide both a source and destination folder.')
        

window.close()