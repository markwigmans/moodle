
# Moodle Processing Scripts

This repository contains useful Python scripts for processing output files from [Moodle](https://moodle.org/). Each subproject is tailored to handle specific types of Moodle files.

## Subprojects Overview

| Project                      | Purpose                                      |
|------------------------------|----------------------------------------------|
| [Essays](./essays/readme.md) | Process essay submissions from students      |
| [Exam](./exam/readme.md)     | Process final exam submissions from students |
| [Forum](./forum/readme.md)   | Process forum posts for marking              |  
| tests                        | unit tests for the different projects        |
| utils                        | generic utils for the the projects           |

## Useful Commands

### Python Environment Management

Package management is handled via [Conda](https://docs.conda.io/projects/conda/en/latest/index.html). Below are some common commands:

- **Clean Environment:**
  - `conda clean -a` - Cleanup the Conda environment.

- **Update Dependencies:**
  - `conda update --all` - Update all Conda dependencies.

- **Export/Import Environment:**
  - `conda env export > environment.yml` - Export the current environment to a YAML file.
  - `conda env update --file environment.yml --prune` - Export the current environment and update the *environment.yml*  file.
  - `conda env create -f environment.yml` - Create an environment from an exported YAML file.

- **Prepare environment for CI/CD:**
  - `pip list --format=freeze > requirements.txt` - - Export the current environment to a pip format/
