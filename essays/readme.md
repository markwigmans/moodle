# Moodle Essay Assignment
Process the files generated from Moodle and create a directory per marker.

# Steps

The following steps must be performed:

1. Copy **config.ini-template** to **config.ini** and change fields accordingly
1. Retrieve data from Moodle
1. Copy all data to config setting ( section 'files', element 'data') directory
1. run main.py

## Moodle Download Settings
Download all submissions for the given activity with the following steps:

1. Goto assignment
1. Press 'View all submissions'
1. Press 'Download all submissions'

# Configuration

| Group  | Field         | Description                                        | Default            |
|--------|---------------|----------------------------------------------------|--------------------|
| grades | file          | Input Excel files with students, marker            | grades.xlsx        |
| grades | worksheet     | Worksheet of *grades.files* file                   | Final Exam         |
| grades | header        | Number of lines of header line, 0 based            | 0                  |
| grades | id_offset     | Offset to be used for the ref number prefix        | 1                  | 
| files  | data          | Input directory with all the student submissions   | data               |
| files  | output        | Output directory submissions ordered by marker     | markers            |
| files  | overview      | Output excel file of process                       | overview.xlsx      |
| files  | not_processed | Output excel file with students without submission | not_processed.xlsx |
| files  | refnr_length  | Length of the file prefix number                   | 2                  |
