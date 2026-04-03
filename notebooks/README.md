## fhir-moldef Educational Notebook Series

This repository includes a set of interactive Jupyter notebooks that provide a hands-on introduction to the 
**fhir-moldef** codebase. The notebooks demonstrate how to work with the **HL7 FHIR MolecularDefinition Resource**, exploring its associated **Profiles**, and perform bidirectional translation between **GA4GH VRS (v2.0)** and **HL7 FHIR MolecularDefinition**.

## Notebook Categories

### 1. **Schema Notebooks** (`notebooks/schemas/`)

- **1.1** **[MolecularDefinition](schemas/01_molecular_definition_overview.ipynb)**  
   - Demonstrates the Python implementation of the HL7 FHIR **MolecularDefinition resource**.  
   - Includes a structured, step-by-step guide for constructing the resource.

- **1.2** **[Sequence Profile](schemas/02_sequence_profile.ipynb)**  
   - Demonstrates the Python implementation of the MolecularDefinition **Sequence profile**, with a step-by-step walkthrough for building a Sequence.

- **1.3** **[Allele Profile](schemas/03_allele_profile.ipynb)**  
   - Demonstrates the Python implementation of the MolecularDefinition **Allele profile**, with a step-by-step walkthrough for building an Allele.

- **1.4** **[Variation Profile](schemas/04_variation_profile.ipynb)**
   - Demonstrates the Python implementation of the MolecularDefinition **Variation profile**, with a step-by-step walkthrough for building a Variation.

### 2. **Translational Notebooks** (`notebooks/translations/`)

- **2.1** **[Simple Allele Creation & Translation](translations/01_simple_allele_creation_and_translation.ipynb)**
   - Shows how the **Allele Builder**, which simplifies the creation of **VRS Allele** object and **FHIR Allele** profile.
   - Instead of requiring detailed knowledge of VRS or FHIR schemas, users provide just **five attributes** to generate valid Allele objects. 
   - The resulting Allele can then be used with the project’s translation tools to convert between **VRS** and **FHIR** representations.

- **2.2** **[VRS to FHIR: Allele Translation](translations/02_vrs_to_fhir_allele_translation.ipynb)**  
   - Demonstrates how **VRS Allele** representations with the **minimal required fields** are converted into **MolDef Allele Profile**.

- **2.3** **[FHIR to VRS: Allele Translation](translations/03_fhir_to_vrs_allele_translation.ipynb)**  
   - Shows how **MolDef Allele Profile** with the **minimal required elements** are translated into **VRS Allele** representations.  

- **2.4** **[Full Allele Translations](translations/04_full_allele_roundtrip_translation.ipynb)**  
   - Demonstrates the **VRSToFHIR** and **FHIRToVRS** modules for translating fully populated **VRS Allele** objects to **MolDef AlleleProfile**, and vice versa.
   - This notebook focuses on **full, schema compliant Alleles** rather than the minimal examples shown in earlier notebooks.

- **2.5** **[SPDI / HGVS to FHIR Variation](translations/05_spdi_hgvs_to_fhir_variation.ipynb)**  
   - Demonstrates how **SPDI** and **HGVS** expressions are translated into **HL7 FHIR Variation** profile resources. 

- **2.6** **[ClinVar Data to FHIR Allele Translation](translations/06_clinvar_vrs_to_fhir_allele_translation.ipynb)**  
   - Demonstrates extraction and translation of ClinVar variation data into HL7 FHIR Allele Profiles.
   - This notebook is intended for **inspection and review only** and is **not designed to be executed end-to-end**. For large-scale translation, use the **`clinvar_translate.py`** pipeline.

<!-- ### **Recommended Knowledge**

To get the most out of these notebooks, we recommend the following prerequisites:
   - Familiarity with **Jupyter Notebook** and **Python**.
   - An understanding of the **HL7 FHIR MolecularDefinition** schema, you can review it here: [FHIR MolecularDefinition Schema](https://build.fhir.org/moleculardefinition.html).
   - Knowledge of the **GA4GH VRS (v2.0)** schema, which is essential for bidirectional translation. Documentation is available here: [GA4GH VRS Schema](https://vrs.ga4gh.org/en/stable/).

For setup instructions, including how to run these notebooks in **Codespaces**, refer to the main project [README](../README.md). -->

## Interacting with Notebooks
To interact with the fhir-moldef, you can use GitHub Codespaces to access and work with the Jupyter Notebooks directly. If you plan to make changes, please fork the repository and submit your suggestions or modifications via an issue and a pull request. Personal accounts receive 120 free hours of Codespaces usage, while Pro accounts receive 180 hours. Be aware that Codespaces has a default timeout period of 30 minutes. For more information about Codespaces, refer to the links provided below. If you're already familiar with Codespaces and Jupyter Notebooks, you can proceed with the instructions below.

If you're new to using **Codespaces**, the following resources may be helpful:
* [Codespaces Overview](https://docs.github.com/en/codespaces/overview)
* [Codespaces Getting Started Documentation](https://docs.github.com/en/codespaces/getting-started/quickstart)

## Access Notebooks (Codespace)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=905915041)

## 1. Starting Codespace
* Start off by clicking the Codespaces badge above to get started.
* A prompt to build a code space will pop up with certain specifications.
* Click on **Create Codespace**.
* **NOTE**: This will take a few minutes to build your virtual machine. A message will appear in the terminal indicating the progress:
    ```bash
    Finishing up...
    Running postCreateCommand...
    ```
* **NOTE**: If you encounter the following GitHub Codespace error:

    > _"Oh no, it looks like you are offline! Make sure you are connected to the internet and try again. If you verified that your connection is fine, your firewall might be blocking the connection."_

    This issue is most likely caused by an active **VPN**. To resolve it:
    
    * Sign out of your **VPN** and try again.
    * If the issue persists, check your security settings or network configuration.

## 2. Selecting Kernel
* Navigate to the notebooks and select a notebook you wish to run.
* Locate the **Select Kernel** option on the top right-hand side of the interface.
* Click on **Select Kernel**.

## 3. Choosing Python Environment
* After clicking **Select Kernel**, a pop-up will appear. Choose **Python Environment...**.
* From the dropdown menu, select:
    ```plaintext
    Python 3.11.11 /usr/local/bin/python
    ```
* **NOTE**: This step must be performed for each notebook that you intend to execute.

## 4. Running Notebooks
* Once the appropriate kernel is selected, you can proceed to run the cells inside the Jupyter notebooks.
* 💡 **Tip**: Use `Shift + Enter` to execute a cell quickly.

## 5. Deactivating Codespace
* On the bottom left corner of your browser, click on **CodeSpaces:** (highlighted in blue).
* A pop-up will appear. Then, click **Stop Current Codespace**.
* Once this is done, you have successfully deactivated your Codespace.

