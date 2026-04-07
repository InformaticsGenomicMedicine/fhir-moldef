# ClinVar VRS Allele to FHIR Translation Pipeline

The variant data used in this project is derived from the ClinVar Genomic Knowledge Standards (GKS) initiative, a ClinGen supported effort to transform ClinVar releases into GA4GH-compliant representations. The data is accessed via public URLs and is hosted in the ClinVar GKS repository on GitHub: [clinvar-gks](https://github.com/clingen-data-model/clinvar-gks). This repository serves as the authoritative source of the ClinVar GKS data used by the pipeline.

This module primarily works with ClinVar variation files. It extracts VRS Allele objects from each record’s members array, validates them against the GA4GH VRS model, and translates valid alleles into the FHIR Allele Profile using the `VrsToFhirAlleleTranslator`.


## What it does
For each line in the input JSONL:

1. Parse JSON.
2. Look for `members` (list).
3. For each member:
   - Keep only objects where `member["type"] == "Allele"`.
   - Validate by constructing a `ga4gh.vrs.models.Allele`.
   - Classify allele state type counts:
     - `LiteralSequenceExpression`
     - `ReferenceLengthExpression`
     - Other
   - Translate to FHIR Allele Profiles via `VrsToFhirAlleleTranslator.translate_allele_to_fhir()`.
4. Write results and errors as JSON Lines.


## Requirements
This pipeline requires access to a SeqRepo instance. Before running the pipeline, ensure that SeqRepo is available and that the GA4GH VRS data proxy environment variable is set to point to the appropriate
SeqRepo resource:

```bash
export GA4GH_VRS_DATAPROXY_URI="seqrepo+file:///path/to/your/seqrepo"
```

## How to run
The translation pipeline is executed using the `clinvar_translator.py` script
located in the `pipeline/` directory.

```bash
python pipeline/clinvar_translator.py path/to/clinvar_variations.jsonl.gz
```