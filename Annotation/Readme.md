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
For the creation of the CACAPO dataset, two different annotation tools were used. Prodigy, and a Tkinter-based tool made from scratch. The Tkinter-based tool is more or less a case of "reinventing the wheel", and it still contains some bugs (for instance, when going back to previous sentences). Furthermore, the Tkinter-based tool does not save the text location of the annotations. Thus, if you feel like applying the annotation process to new domains, I would advise using Prodigy.

In any case, the following domains use the Tkinter-based tool:
- Incidents (NL)
- Sports (NL)
- Incidents (EN)

The other domains were annotated using Prodigy.

<h2>Tkinter-based tool</h2>

The domains using the Tkinter-based tool contain the following scripts:

1. Create_Pickles --> Reformats the original texts into an annotation-friendly format.
2. Data_Annotation --> The main tool: used to annotate the data for the sentences.
3. Train_Dev_Test_Split --> Split the annotated sentences up into a train, development, and test set.
4. Convert_Formats --> Output the annotated sentences into a [SQuAD 2.0](https://rajpurkar.github.io/SQuAD-explorer/), [WebNLG](https://webnlg-challenge.loria.fr/), [CoNLL-2003](https://github.com/huggingface/transformers/tree/main/examples/pytorch/token-classification/), [TRECQA](https://github.com/Kyung-Min/CompareModels_TRECQA/), or a format suitable for a classification model.



1. The whole message, with the current sentence in bold
2. The current sentence. Here you can also make changes to the sentence.
3. Add new data type: type the name of the new data type in this bar and then press "Add data type".
4. Clear data type selection: if there are errors in the annotated data of that sentence, you can press this button to start over. It clears the current selection of selected data points.
5. The bar with which you select the data types. This is also where you copy the text passage where the data is located.
6. Save. Save the information of the current sentence.
7. Previous. If you consider that there are errors in an earlier sentence, you can go to this sentence.
8. Skip sentence. If it is a sentence that should not be in the text, you can press it. So you only use this for sentences that should not be part of the text (for example URLs). For sentences that belong in the text, but that do not contain any information, press save without annotating any further information.
9. Skip text. If this text is not suitable for the corpus, you can press it.
