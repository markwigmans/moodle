# Moodle

Useful python scripts to process [Moodle](https://moodle.org/) output files.

The subprojects are able to process particular Moodle files:

| project                      | purpose                                     | 
|------------------------------|---------------------------------------------| 
| [essays](./essays/readme.md) | Process essay submission from students      | 
| [exam](./exam/readme.md)     | Process final exam submission from students | 
| [forum](./forum/readme.md)   | Process forum posts to be marked            |

# Useful commands

## Package Management

Package management is done via [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)

- `conda clean -a` : cleanup the environment
- `conda update --all` : update all dependencies
- `conda env export > environment.yml` : export environment
- `conda env create -f environment.yml` : import environment