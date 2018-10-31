# TEITransformations
Scripts to:
- transform multiple TEI XML files into single TEI XML files (root : TEI)
- transform multiple TEI XML files into single TEI XML files (root : teiCorpus)

Both scripts expect TEI XML files created with `ExportFromTranskribus` project with specific forms.

## Getting started

### Prerequisites
- `tei2tei.py` expects, in ` <title>`, a title form with the following model: "{Title}, {number}, page {pagenumber} - Transcription" ;
- `tei2teicorpus.py` expects, in `<title>`, a title form with the following model: "{Title}, {number} - Transcription" ; 

Where {number} refers to a volume. This is because they were initially designed to transform newpapers transcriptions. 


### Installing
- use virtual environment with Python3 and requirements installed
- create `input` and `output` directories in `TEI2TEI` and `TEI2TEICORPUS` directories to store and retrieve your data

### Running

#### TEI2TEI

```
(.venv)~$ python3 tei2tei.py
//will keep facsimile elements and related attributes

(.venv)~$ python3 tei2tei.py -nofacs
// will ignore facsimile elements and related attributes
```

#### TEI2TEICORPUS
```
(.venv)~$ python3 tei2teicorpus.py
// will perform transformation after asking for an output title
``` 
