# ANNOTATION
Files for the data annotation step for creating the CACAPO dataset

<h2>Installation</h2>

For all the data annotation steps, you need the following libraries:

[Regex](https://pypi.org/project/regex/)<br/>
[lxml](https://pypi.org/project/lxml/)<br/>
[Pattern](https://www.clips.uantwerpen.be/pages/pattern/)<br/>
[openpyxl](https://pypi.org/project/openpyxl/)<br/>
[spaCy](https://spacy.io/usage/)<br/>
[SoMaJo](https://github.com/tsproisl/SoMaJo)<br/>
[pySBD](https://github.com/nipunsadvilkar/pySBD)<br/>
[pyperclip](https://pypi.org/project/pyperclip/)<br/>
[Prodigy](https://prodi.gy/)<br/>

<h2>Two annotation tools</h2>
For the creation of the CACAPO dataset, two different annotation tools were used. Prodigy, and a manually created tool. The manually created tool is a bit of a case of "reinventing the wheel", and it still contains some bugs (regarding going back to previous sentences) and the build does not save the text location of the annotations. So I would advise using Prodigy.
