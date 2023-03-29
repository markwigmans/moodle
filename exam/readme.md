# Moodle Exam
Process the files generated from Moodle and create a directory per grader.

# Steps

The following steps must be performed:

1. Copy 'config.ini-template' to 'config.ini' and change fields accordingly
1. Retrieve data from Moodle
1. Copy all data to config setting [files][data] directory
1. run main.py

## "Moodle Download Settings

| Setting                    | Value               | 
| -------------------------- | ------------------- |
| Set folder hierarchy       | Essay question wise | 
| Include text response file | Yes                 |
| Include question text file | Yes                 |

# Configuration

| Group  | Field         | Description                                        | Default            |
| ------ | ------------- | -------------------------------------------------- | ------------------ |
| grades | file          | Input Excel files with students, marker            | grades.xlsx        |
| grades | worksheet     | Worksheet of grades.files file                     | Final Exam         |
| grades | header        | Number of lines of header line, 0 based            | 0                  |
| files  | data          | Input directory with all the student submissions   | data               |
| files  | output        | Output directory submissions ordered by marker     | markers            |
| files  | overview      | Output excel file of process                       | overview.xlsx      |
| files  | not_processed | Output excel file with students without submission | not_processed.xlsx |
