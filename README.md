<h1 align="center">fhir-moldef</h1>

## Overview

Welcome to the **fhir-moldef** repository. This project provides a Python implementation of the HL7 (Health Level Seven) Fast Healthcare Interoperability Resources (FHIR) Molecular Definition standard. It enables users to create instances of the MolecularDefinition resource and currently supports three profiles: Sequence, Allele, and Variant.

<!--In FHIR, a profile is a structured extension of a resource that defines specific constraints and usage guidelines for particular use cases. -->

Additionally, this repository supports seamless, bidirectional translation between Global Alliance for Genomics and Health (GA4GH) Variant Representation Specification (VRS) Alleles (v2.0) and the FHIR Allele Profile, enabling interoperability between the two standards.

<!-- To help you get started, we provide Jupyter notebooks that serve as an educational guide. These notebooks introduce the MolecularDefinition resource, explain its profiles, and showcase the translation process between VRS Alleles (v2.0) and FHIR Allele with practical examples. -->


## Disclaimer

This project uses the `MolecularDefinition` schema from the latest in-progress development version: [Work in Progress Schema](https://build.fhir.org/branches/cg-im-moldef_work_in_progress_2/moleculardefinition.html). This page may occasionally be unavailable due to active development.

It does **not** match the schema in the HL7 FHIR 6.0.0 Ballot 2 release: [FHIR Ballot 2 Schema](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html).

<!-- * **Note**: The [Work in Progress Schema](https://build.fhir.org/branches/cg-im-moldef_work_in_progress_2/moleculardefinition.html) page may occasionally be unavailable due to active development. This downtime is beyond our group's control. If the page is temporarily inaccessible, we recommend trying again later. -->

## Core Functionality

| Category | Currently Supported |
|----------|---------------------|
| **Resource** | Generation of HL7 FHIR MolecularDefinition resources |
| **Profiles** | Sequence, Allele, and Variant profiles |
| **Translation** | Bidirectional translation between VRS 2.0 and FHIR (full + minimal) |
| **Notebooks** | Interactive Jupyter notebooks with examples (**see the Notebooks README for details**) |
| **Pipeline** | Extraction of VRS Allele objects from ClinVar variation files and translation into the FHIR Allele Profile |

<!-- ## Features

### Resource
* **Generation of Molecular Definition Resources**: Effortlessly create fully compliant Molecular Definition resources based on the HL7 FHIR standard.

### Profile
* **Sequence**: Sequence is a specialized subclass of the MolecularDefinition resource, enabling you to create sequence-specific representations.

* **Allele**: Allele is a specialized subclass of the MolecularDefinition resource, allowing you to create and manage allele-specific representations.

### Translation
* **Bidirectional Translation**: Perform seamless, bidirectional translations between FHIR Allele and VRS Alleles (version 2.0), ensuring interoperability and data consistency across diverse platforms.

### Notebooks
* **Educational Jupyter Notebooks**: Access interactive Jupyter notebooks for a hands-on learning experience, complete with practical examples and educational insights into the implementation’s functionality. -->

## Installation Status

This package is not currently published on PyPI but will be available soon.  
In the meantime, clone the repository and follow the instructions below to work with the code locally.

## Prerequisites

- **Python 3.11–3.13**
- **Virtual environment (uv recommended)**: used to manage project dependencies

## Dependencies & Infrastructure

The following infrastructure is required **only for the VRS ↔ FHIR translation functionality**:

- **PostgreSQL 14**
- **SeqRepo (`biocommons.seqrepo`)**

These dependencies are **not required** if you only plan to instantiate MolecularDefinition profiles.

For instructions on installing and configuring SeqRepo, see the [VRS-Python SeqRepo installation guide](https://github.com/ga4gh/vrs-python).

Containerized setup instructions using **Podman** are planned, including configuration for running SeqRepo (and future UTA support).

<!-- Additional documentation for installing SeqRepo locally is in development. A **docker-compose.yml** configuration will also be provided to run SeqRepo (and future UTA support) in a containerized environment.-->

<!-- ## Local Setup

Follow these steps to set up the project for local development.

### 1. Clone the Repository
Make sure you’re logged into GitHub, then clone the repository and navigate into it:

```bash
git clone https://github.com/YourUsername/fhir-moldef.git
cd fhir-moldef
```

### 2. Create and Activate a Virtual Environment
We recommend using Python’s built-in `venv` module.

   ```bash
   python -m venv venv
   ```

Activate the virtual environment

- **macOS/Linux**
   ```bash
   source venv/bin/activate
   ```
- **Windows** 
   ```bash
   venv\Scripts\activate
   ```

### 3. Install the Package
- **Installation (until the package is published)**
   ```bash
   pip install . 
   ```

- **Local Development**
   ```bash
   pip install -e .[dev]
   ```

### 4. Verify Installation
Confirm the package was installed successfully
   ```bash
   pip show fhir-moldef
   ``` -->

## Local Setup

Clone the repository and install the package for local development.

```bash
git clone https://github.com/YourUsername/fhir-moldef.git
cd fhir-moldef

uv venv
source .venv/bin/activate

uv pip install -e .[dev]
```

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit a pull request.  
You can also report bugs or suggest improvements by opening an issue.

## Acknowledgments

This project builds upon the following community standards and open-source implementations.

### Standards

- [GA4GH Variation Representation Specification (VRS)](https://vrs.ga4gh.org/)
- [HL7 FHIR MolecularDefinition](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html)

### Software

- [vrs-python](https://github.com/ga4gh/vrs-python)
- [biocommons.seqrepo](https://github.com/biocommons/biocommons.seqrepo)
- [fhir.resources](https://github.com/nazrulworld/fhir.resources)
- [fhir-core](https://github.com/nazrulworld/fhir-core)

We gratefully acknowledge the communities and contributors who develop and maintain these standards and software projects.