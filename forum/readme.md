# Moodle Forum
Process the files generated from Moodle forums and create an overview about the posts per student.
Useful for forums were students get marks for posts in a given forum.

# Steps

The following steps must be performed:

1. Copy **config.ini-template** to **config.ini** and change fields accordingly
1. perform for every Moodle forum
   1. Retrieve data from Moodle
   1. Copy export data to config setting ( section 'forum.', element 'file') location
1. run main.py

## "Moodle Forum Download Settings

Goto the given forum and choose 'export' with the given settings:

| Setting              | Value                     | 
|----------------------|---------------------------|
| Users                | All users (default)       |
| Discussions          | All discussions (default) |
| Format               | CSV (default)             |
| Remove HTML          | Yes                       | 
| Human-readable dates | Yes                       |

# Configuration

| Group    | Field       | Description                                            | Default                 |
|----------|-------------|--------------------------------------------------------|-------------------------|
| students | file        | Input Excel files with students, marker                | students.xlsx           |
| students | worksheet   | Worksheet with 'participation' information to be found | Quizzes - Participation |
| output   | file        | output Excel with overall result                       | participation.xlsx      |
| forum.   | title       | title used as worksheet description                    |                         |
| forum.   | description | Description of forum to be used in 'readme' worksheet  |                         |
| forum.   | file        | CSV file with postings of given forum                  |                         |

The 'forum.' part can be *repeated*. 