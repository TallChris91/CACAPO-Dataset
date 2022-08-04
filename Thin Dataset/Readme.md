# Thin Dataset
Thin dataset files and tool to collect new texts.

## The thin dataset files

All domains contain 2 files:

- A JSON file containing all the original annotations with references to the original text
- A sqlite file that contains information on the sources of the original texts (as far as this was possible, some domains are missing information due to coming from different sources)

## Installation

For the collection tool, you need the following libraries: 
- [Pyperclip](https://pypi.org/project/pyperclip/)
- [Ruamel.std.zipfile](https://pypi.org/project/ruamel.std.zipfile/)
- [Regex](https://pypi.org/project/regex/)
- [Selenium](https://pypi.org/project/selenium/)
- [Python-dateutil](https://pypi.org/project/python-dateutil/)

## Using the save tool

The tool to collect texts is TKinter-based and looks as follows:

![alt text](https://github.com/TallChris91/CACAPO-Dataset/blob/main/Thin%20Dataset/Opslatool.png "Save tool")

## How to fill in the save tool:

1.	Copy the writer to the first field (if there is a writer on the website)
2.	Copy the publish date to the second field (Generally, every format works as long as you only copy day, month and year. Things like the day of the week, and time of day may not be saved in the correct format)
3.	Copy the text to the third field
4.	Press ‘Opslaan’. You should get a message such as '<filename> toegevoegd aan de database'.
6.	If you are done, you can press ‘Afsluiten’.

You can copy by Ctrl-V in the fields, or by pressing the button next to the fields.

The tool should save a sqlite database, as well as a zipfile containing all relevant data.
