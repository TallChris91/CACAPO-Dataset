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

![alt text](https://github.com/TallChris91/CACAPO-Dataset/blob/main/Annotation/Annotationtool.png "Annotation tool")

The annotation tool contains the following elements:

1. The whole message, with the current sentence in bold
2. The current sentence. Here you can also make changes to the sentence.
3. Add new data type: type the name of the new data type in this bar and then press "Add data type".
4. Clear data type selection: if there are errors in the annotated data of that sentence, you can press this button to start over. It clears the current selection of selected data points.
5. The bar with which you select the data types. This is also where you copy the text passage where the data is located.
6. Save. Save the information of the current sentence.
7. Previous. If you consider that there are errors in an earlier sentence, you can go to this sentence.
8. Skip sentence. If it is a sentence that should not be in the text, you can press it. So you only use this for sentences that should not be part of the text (for example URLs). For sentences that belong in the text, but that do not contain any information, press save without annotating any further information.
9. Skip text. If this text is not suitable for the corpus, you can press it.

<h3>Other things</h3>

- "Previous" sometimes gives errors if you go back to a previous text and had skipped sentences. So be careful with that.
- Sometimes when you change the data types in the pop-up bar, it gives problems with annotation afterwards. This is a bug. If you encounter this problem, it is best to press "Remove data type selection" and annotate the sentence again.
- The sentence splitter is not perfect. Especially passages like <i>"3 p.m. Sunday"</i> are often split into two sentences. What I do then is paste the second part of the sentence (<i>Sunday</i>) after the first sentence (<i>3 p.m.</i>) in "Current Sentence". I then annotate the entire sentence and save it. Then you get to see the second part of the sentence again and there you press "Skip sentence".
- You often have multiple passages about the same data type. For example, in a sentence like <i>"This happened early Sunday on the Brooklyn Bridge at 3 p.m."</i> The passages "early Sunday" and "3 p.m." both are about the date. To include both passages, add both passages to the date label, with ";;" (2 semicolons) in between. So "early Sunday;;3 p.m." This double separator tells the script that there are two separate passages in the sentence it needs to look for. Even if the passages are the same word, e.g. <i>"Witnesses say four people were injured, but all four of them were in stable condition"</i> in this case enter "four;; four" for victimNumber.

<h2>Prodigy annotation</h2>

The domains using Prodigy contain the following scripts:

1. Create_Jsonl --> Reformats the original texts into a Jsonl-format that is usable by Prodigy.
2. Prodigy_Commands --> The main tool: runs the terminal commands to start the Prodigy server. Make sure to lead the virtual environment line to a virtual environment that has Prodigy and spaCy (with the relevant models) installed.
3. Train_Dev_Test_Split --> Split the annotated sentences up into a train, development, and test set.
4. Add_Paragraph_Sentence_Info --> Add the paragraph and sentence index of the annotated data. Important for the SQuAD 2.0 format.
4. Convert_Formats --> Output the annotated sentences into a [SQuAD 2.0](https://rajpurkar.github.io/SQuAD-explorer/), [WebNLG](https://webnlg-challenge.loria.fr/), [CoNLL-2003](https://github.com/huggingface/transformers/tree/main/examples/pytorch/token-classification/), [TRECQA](https://github.com/Kyung-Min/CompareModels_TRECQA/), or a format suitable for a classification model.

Prodigy's annotation system is quite straightforward.
