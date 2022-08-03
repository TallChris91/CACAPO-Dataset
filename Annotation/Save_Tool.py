import tkinter as tk
import pyperclip
import ruamel.std.zipfile as zipfile
import json
import sqlite3
import time
import os
import regex as re

def clean_text(text):
    #performs a few cleaning steps to remove non-alphabetic characters

    #replace new line and carriage return with space
    text = text.replace("\n", " ").replace("\r", " ")
    #replace the numbers and punctuation (exclude single quote) with space
    punc_list = '!"#$%&()**+,-./:;<=>?@[\]^_{|}~' + '0123456789'
    t = str.maketrans(dict.fromkeys(punc_list, " "))
    text = text.translate(t)

    #replace single quote with empty character
    t = str.maketrans(dict.fromkeys("'`", ""))
    text = text.translate(t)

    return text

def word_tokenize(text):
    #Make a list of all the existing words
    WORD = re.compile(r'\w+')
    #Clean all punctuation, etc.
    text = clean_text(text)
    #And find all words
    words = WORD.findall(text)
    return words

def add_file(zipname, fileinfo, filename, overwrite='n'):
    readzip = zipfile.ZipFile(zipname)
    #Write the playerinfo file if there is no file for the player yet, or if overwrite is on
    if (filename not in readzip.namelist()) or (overwrite == 'y'):
        #Delete the previous file with the same filename if overwrite is on
        if filename in readzip.namelist():
            zipfile.delete_from_zip_file(zipname, filename)
        with zipfile.ZipFile(zipname, 'a') as zipped_f:
            zipped_f.writestr(filename, json.dumps(fileinfo, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8'))
    readzip.close()

def create_project(conn, project):
    # create table
    #Change "weather" to the relevant domain
    sql = '''CREATE TABLE weather (byline, postdate, edition, postlanguage, postlength, loaddate, newspaper, publicationtype, section, subject, text, title, filename)'''
    insert = '''INSERT INTO weather (byline, postdate, edition, postlanguage, postlength, loaddate, newspaper, publicationtype, section, subject, text, title, filename) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(insert, project)
    '''
    while True:
        try:
            cur.execute(sql)
            break
        except sqlite3.OperationalError:
            time.sleep(1)
    while True:
        try:
            cur.execute(insert, project)
            break
        except sqlite3.OperationalError:
            time.sleep(1)
    '''


def extend_project(conn, project):
    # Change "weather" to the relevant domain
    sql = '''INSERT INTO weather (byline, postdate, edition, postlanguage, postlength, loaddate, newspaper, publicationtype, section, subject, text, title, filename) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    #Try to find out whether the table exists
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='weather' ''')
    #If it does, add new entry to the table
    if cur.fetchone()[0] == 1:
        while True:
            try:
                cur.execute(sql, project)
                break
            except sqlite3.OperationalError:
                time.sleep(1)
    #If it does not, create the table
    else:
        create_project(conn, project)


def database_main(db, dbinfo):
    if os.path.exists(db) == True:
        # create a database connection
        with sqlite3.connect(db) as conn:
            # extend the project
            extend_project(conn, dbinfo)
    else:
        with sqlite3.connect(db) as conn:
            create_project(conn, dbinfo)

def database_search(db, searchword):
    #If there is no database yet, return notFound
    if not os.path.exists(db):
        return 'notFound'

    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        # Try to find out whether the table exists
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='weather' ''')
        # If it does not, return notFound
        if cur.fetchone()[0] == 0:
            return 'notFound'

        while True:
            try:
                cur.execute("SELECT * FROM weather WHERE text = ?", (searchword,))
                break
            except sqlite3.OperationalError:
                time.sleep(1)
        data = cur.fetchone()
        if data is None:
            return 'notFound'
        else:
            #Return the filename
            return data[-1]

def database_search_filename(db, searchword):
    #If there is no database yet, return notFound
    if not os.path.exists(db):
        return 'notFound'

    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        # Try to find out whether the table exists
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='weather' ''')
        # If it does not, return notFound
        if cur.fetchone()[0] == 0:
            return 'notFound'

        while True:
            try:
                cur.execute("SELECT * FROM weather WHERE filename = ?", (searchword,))
                break
            except sqlite3.OperationalError:
                time.sleep(1)
        data = cur.fetchone()
        if data is None:
            return 'notFound'
        else:
            #Return the filename
            return data[-1]

def convertdate(date):
    #Function that convert dates like 20 oktober 2018 13:22 to 20-10-2018
    monthdict = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
                 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
    #Find the part up until the year
    #date = re.search(r'^(.*?)20(\d\d)', date).group()
    #Split days, months and years
    date = date.split()
    #Convert the month using the above dictionary
    #Most of the time you have stuff like 24 september 2019 dinsdag
    try:
        newmonth = monthdict[date[1].lower()]
    except KeyError:
        monthdict = {'jan.': '01', 'feb.': '02', 'mrt.': '03', 'apr.': '04', 'mei': '05', 'jun.': '06',
                     'jul.': '07', 'aug.': '08', 'sep.': '09', 'okt.': '10', 'nov.': '11', 'dec.': '12'}
        newmonth = monthdict[date[1].lower()]
    # Put the day, month and year in the right format
    newdate = date[0] + '-' + newmonth + '-' + date[2]

    return newdate

def text_field_paste():
    #Paste the copied value in the text field
    text_field.delete(1.0, tk.END)
    text_field.insert(tk.END, pyperclip.paste())

def name_field_paste():
    # Paste the copied value in the name field
    name_field.delete(0, tk.END)
    name_field.insert(tk.END, pyperclip.paste())

def publish_date_field_paste():
    # Paste the copied value in the publish date field
    publish_date_field.delete(0, tk.END)
    publish_date_field.insert(tk.END, pyperclip.paste())

def newspaper_field_paste():
    # Paste the copied value in the newspaper field
    newspaper_field.delete(0, tk.END)
    newspaper_field.insert(tk.END, pyperclip.paste())

def title_field_paste():
    # Paste the copied value in the title field
    title_field.delete(0, tk.END)
    title_field.insert(tk.END, pyperclip.paste())

def save_values():
    #If the newspaper field is empty, show a message in the save field
    if newspaper_field.get() == '':
        save_field.delete(0, tk.END)
        save_field.insert(tk.END, 'Vergeet niet om de website in te vullen')
    # If the text field is empty, show a message in the save field
    if str(text_field.get(1.0, tk.END)) == '':
        save_field.delete(0, tk.END)
        save_field.insert(tk.END, 'Vergeet niet om de tekst in te vullen')
    else:
        #Get all the values in the gui and supplement this with other values
        byline = name_field.get()
        postdate = publish_date_field.get()
        postdate = convertdate(postdate)
        edition = ''
        postlanguage = 'ENGLISH; ENGELS'
        postlength = word_tokenize(str(text_field.get(1.0, tk.END)))
        postlength = str(len(postlength)) + ' words'
        # Get the current date for the scrape date
        loaddate = time.strftime("%d-%m-%Y")
        newspaper = newspaper_field.get()
        publicationtype = 'Web Publicatie'
        sec = 'Weather'
        subject = ''
        textstring = str(text_field.get(1.0, tk.END))
        title = title_field.get()


        filenamenewspaper = re.sub(r'https://www.', '', newspaper_field.get())
        filenamenewspaper = re.sub(r'www.', '', filenamenewspaper)
        filenamenewspaper = re.sub(r'https://', '', filenamenewspaper)
        filenamenewspaper = re.search(r'^(.*?)(\/|$)', filenamenewspaper).group(1)

        # Convert the newspaper name and date to a filename
        # Get the newspaper name and change punctuation to an underscore
        filenamenewspaper = re.sub(r"\p{P}+", '_', filenamenewspaper)
        # Change spaces to an underscore
        filenamenewspaper = re.sub(r"\s+", '_', filenamenewspaper)
        # Convert a date like 20-10-2018 to 20102018 for the filename
        filenamedate = re.sub(r"-", '', postdate)
        # Now we have a filename like NRC_Next_20102018.txt
        filename = filenamenewspaper + '_' + filenamedate + '.json'

        # Change "weather" and "(English)" to the relevant domain and language, respectively
        # See if we can find the filename, if we can find it, we need to get a new filename
        if database_search_filename(os.getcwd() + '/Data/WeatherDB(English).db', filename) != 'notFound':
            # Otherwise, add (2) or (3), etc. to the filename (the first number, starting at 2, that is not already a filename, is chosen)
            for i in range(2, 9999):
                newfilename = filenamenewspaper + '_' + filenamedate + '(' + str(i) + ').json'
                # If the new filename is not used before, we will use it as our filename value
                if database_search_filename(os.getcwd() + '/Data/WeatherDB(English).db', newfilename) == 'notFound':
                    filename = newfilename
                    break

        searchdatabase = database_search(os.getcwd() + '/Data/WeatherDB(English).db', textstring)

        if searchdatabase != 'notFound':
            print('File already exists (' + searchdatabase + ')')
            save_field.delete(0, tk.END)
            save_field.insert(tk.END, filename + ' bestaat al')

        sqllist = [byline, postdate, edition, postlanguage, postlength, loaddate, newspaper, publicationtype, sec, subject, textstring, title, filename]

        database_main(os.getcwd() + '/Data/WeatherDB(English).db', sqllist)
        print(filename + ' added to the database')

        sqldict = {'byline': byline, 'date': postdate, 'edition': edition, 'language': postlanguage, 'length': postlength, 'load-date': loaddate,
                   'newspaper': newspaper,
                   'publication-type': publicationtype, 'section': sec, 'subject': subject, 'text': textstring, 'title': title, 'filename': filename}
        if not os.path.isfile(os.getcwd() + '/Data/EnglishWeatherReports.zip'):
            zf = zipfile.ZipFile(os.getcwd() + '/Data/EnglishWeatherReports.zip', mode='w')
            zf.close()

        add_file(os.getcwd() + '/Data/EnglishWeatherReports.zip', sqldict, filename)
        print('File saved (' + filename + ')')

        save_field.delete(0, tk.END)
        save_field.insert(tk.END, filename + ' toegevoegd aan de database')

        name_field.delete(0, tk.END)
        publish_date_field.delete(0, tk.END)
        newspaper_field.delete(0, tk.END)
        title_field.delete(0, tk.END)
        text_field.delete(1.0, tk.END)


name_field = ''
publish_date_field = ''
newspaper_field = ''
title_field = ''
text_field = ''

# create a GUI window
gui = tk.Tk()

# set the title of GUI window
gui.title("Save news articles")

namevar = tk.StringVar()
name_field = tk.Entry(gui, textvariable=namevar)
name_button = tk.Button(gui, text='Writer:', command=name_field_paste)
name_button.grid(row=0, column=0, sticky='nesw')
name_field.grid(row=0, column=1, columnspan=5, sticky='nesw')

publish_date_var = tk.StringVar()
publish_date_field = tk.Entry(gui, textvariable=publish_date_var)
publish_date_button = tk.Button(gui, text='Publication date:', command=publish_date_field_paste)
publish_date_button.grid(row=1, column=0, sticky='nesw')
publish_date_field.grid(row=1, column=1, columnspan=5, sticky='nesw')

newspaper_var = tk.StringVar()
newspaper_field = tk.Entry(gui, textvariable=newspaper_var)
newspaper_button = tk.Button(gui, text='Website:', command=newspaper_field_paste)
newspaper_button.grid(row=2, column=0, sticky='nesw')
newspaper_field.grid(row=2, column=1, columnspan=5, sticky='nesw')

title_var = tk.StringVar()
title_field = tk.Entry(gui, textvariable=title_var)
title_button = tk.Button(gui, text='Title:', command=title_field_paste)
title_button.grid(row=3, column=0, sticky='nesw')
title_field.grid(row=3, column=1, columnspan=5, sticky='nesw')

# create the text box for showing an example response.
scroll = tk.Scrollbar(gui)
text_field = tk.Text(gui, height=20, width=50, wrap=tk.WORD)
text_button = tk.Button(gui, text='Text:', command=text_field_paste)
text_button.grid(row=4, column=0, sticky='nesw')
text_field.grid(row=4, column=1, columnspan=5)
scroll.grid(row=4, column=7, sticky='ns')
scroll.config(command=text_field.yview)
text_field.config(yscrollcommand=scroll.set)

save_var = tk.StringVar()
save_field = tk.Entry(gui, textvariable=save_var)
save_button = tk.Button(gui, text='Save:', command=save_values)
save_button.grid(row=5, column=0, sticky='nesw')
save_field.grid(row=5, column=1, columnspan=5, sticky='nesw')
save_field.delete(0, tk.END)
save_field.insert(tk.END, 'Result appears here...')


# start the GUI
gui.mainloop()