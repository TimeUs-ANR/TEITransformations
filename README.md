# TEITransformations
Scripts to:
- transform multiple TEI XML files into single TEI XML files (root : TEI)
- transform multiple TEI XML files into single TEI XML files (root : teiCorpus)

Both scripts expect TEI XML files created with `ExportFromTranskribus` project with specific patterns.

## Getting started

### Prerequisites
- `tei2tei.py` expects, in ` <title>`, a title form with the following model: "{Title}, {number}, page {pagenumber} - Transcription" ;
- `tei2teicorpus.py` expects, in `<title>`, a title form with the following model: "{Title}, {number} - Transcription" ; 

Where {number} refers to a volume. This is because they were initially designed to transform newpapers transcriptions. 

### Input formats
- `tei2tei.py` expects **directories** containing TEI XML files in `input/`. Each directories forms a bundle merged into an output TEI XML file.
- `tei2teicorpus.py` expects **TEI XML files** in `input/`. All files in the directory will be merged into the output TEI XML file.

### Installing
- use virtual environment with Python3 and requirements installed
- create `input` and `output` directories in `TEI2TEI` and `TEI2TEICORPUS` directories to store and retrieve your data, or use --input/--output options to specify other directories.

### Running

#### TEI2TEI
TEI2TEI can transform groups of XML files according to different features. 

```
// By default, tei2tei.py will merge xml files contained in a directory placed in a directory named input/ and will place the result in a directory named output/ 
// both input/ and output/ are expected to be in the same directory as tei2tei.py.

(.venv)~$ python3 tei2tei.py

// You can specify the directory containing the groups of files to merge and/or the directory where the result of the transformations should be placed using --input/-i and/or --output/-o options:

(.venv)~$ python3 tei2tei.py --input directory/name --output directory/name

// ADDITIONAL OPTIONS:

// --nofacs/-n will cause the script to ignore facsimile elements and related attributes:

(.venv)~$ python3 tei2tei.py --nofacs

// --volumes/-v will cause the script to use volume numbers and not complete title to create values to xml:ids in facsimile elements and related
// it is designed for files that are part of the same series and that are numbered accordingly, as unique volumes in the series
// use this option if your titles are formed according to the following pattern : "{title}, {unique\_number}, page {page\_number} - Transcription"
// do not use this option if your series includes several times the same volume number!
// this option will have no effect if the --nofacs/-n option is activated. 

(.venv)~$ python3 tei2tei.py --volumes

```

#### TEI2TEICORPUS
```
// By default, tei2teicorpus.py will merge xml files contained in a directory named input/ and will place the result in a directory named output/, both expected to be in the same directory as tei2teicorpus.py.
 
(.venv)~$ python3 tei2teicorpus.py

// You can specify the directory containing the files to merge and/or the directory where the result of the transformation should be place using --input/-i and/or --output/-o options:

(.venv)~$ python3 tei2teicorpus.py --input directory/name --output directory/name

// By default, the TEI elements in the final teiCorpus will be ordered randomly. You can use addition options to better control the ordering of the TEI elements:

// ADDITIONAL OPTIONS:

// --volumes/-v will cause the script to use volume numbers in ascending order to sort the TEI elements
// It is designed for files that are part of the same series and that are numbered accordingly, as unique volumes in the series
// use this option if your titles are formed according to the following pattern: "{title}, {unique\_number}, page {page\_number} - Transcription"
// do not use this option if your series includes several times the same volume number or they will be overwritten!

(.venv)~$ python3 tei2teicorpus.py --volumes

// --sort/-s will cause the script to use file names in ascending order to sort TEI elements
// WARNING: this option required filenames to be numbers that you manually added

(.venv)~$ python3 tei2teicorpus.py --sort

// --sort/-s and --volumes/-v are NOT compatible
``` 



