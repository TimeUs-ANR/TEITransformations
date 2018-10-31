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

### Input formats
- `tei2tei.py` expects **directories** containing TEI XML files in `input/`. Each directories forms a bundle merged into an output TEI XML file.
-  `tei2teicorpus.py` expects **TEI XML files** in `input/`. All files in the directory will be merged into the output TEI XML file.

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
