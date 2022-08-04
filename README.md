# The CACAPO Dataset

CACAPO is a data-to-text dataset that contains sentences from news reports for the sports, weather, stock, and incidents domain in English and Dutch, aligned with relevant attribute-value paired data. This is the first data-to-text dataset based on "naturally occurring" human-written texts (i.e., texts that were not collected in a task-based setting), that covers various domains, as well as multiple languages. A description of the dataset can be found [here](https://aclanthology.org/2020.inlg-1.10).

<h2>This GitHub page</h2>
This GitHub page contains the "thin" version of the texts in the dataset, which means the annotated data, combined with links to the collected texts. Furthermore it contains the tools used to collect these texts and tools to calculate statistics for the dataset.

<h2>The full dataset</h2>

The full dataset is available via 
[DataVerse](https://doi.org/10.34894/LIBYHP). The format is the same as that of [(Enriched) WebNLG](https://github.com/ThiagoCF05/webnlg) (v1.5). Meaning that the dataset consists of XML files that also contain intermediate representations to enable the development and evaluation of pipeline data-to-text architectures that encompass tasks such as Discourse Ordering, Lexicalization, Aggregation and Referring Expression Generation.

<h2>Example</h2>

```xml
<entry category="EnglishIncidents" eid="Id118" size="2">
  <originaltripleset>
    <otriple>victimAge | 22-year-old</otriple>
    <otriple>victimStatus | grazed_in_the_thigh</otriple>
  </originaltripleset>
  <modifiedtripleset>
    <mtriple>victimAge | 22-year-old</mtriple>
    <mtriple>victimStatus | grazed_in_the_thigh</mtriple>
	</modifiedtripleset>
  <lex comment="good" lid="Id1">
    <sortedtripleset>
      <sentence ID="1">
        <striple>victimAge | 22-year-old</striple>
        <striple>victimStatus | grazed_in_the_thigh</striple>
      </sentence>
    </sortedtripleset>
    <references>
      <reference entity="22-year-old" number="1" tag="PATIENT-1" type="description">A 22-year-old</reference>
      <reference entity="grazed_in_the_thigh" number="2" tag="PATIENT-2" type="description">grazed in the thigh</reference>
    </references>
    <text>A 22-year-old was grazed in the thigh</text>
    <template>PATIENT-1 was PATIENT-2</template>
    <lexicalization>PATIENT-1 VP[aspect=simple,tense=past,voice=active,person=null,number=singular] be PATIENT-2</lexicalization>
  </lex>
  <entitymap>
    <entity>PATIENT-1 | 22-year-old</entity>
    <entity>PATIENT-2 | grazed_in_the_thigh</entity>
  </entitymap>
</entry>
```

<h2>The name "CACAPO"</h2>

<img src="https://github.com/TallChris91/CACAPO-Dataset/blob/main/Kakapo.jpg" alt="A kakapo" width="500"/>
<sub><sup><i>Credits: Andrew Digby, Twitter: @takapodigs</i></sup></sub><br/><br/>

We are aware that the acronym for this dataset is far-fetched, and have also been made aware that the name is phonetically similar to a naughty French word. However, the name of the dataset is a thinly-veiled excuse to raise awareness for the [Kākāpō](https://en.wikipedia.org/wiki/K%C4%81k%C4%81p%C5%8D). The kākāpō is the world's only flightless parrot, and unfortunately, they are critically endangered. There are only 197 kākāpō alive today, but it is not too late to save this beautiful animal from extinction. 

If you would like to support the conservation efforts, you can <b>[donate to Kākāpō Recovery](https://www.doc.govt.nz/our-work/kakapo-recovery/get-involved/donate/)</b>.
