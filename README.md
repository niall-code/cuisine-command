# Cuisine Command

Cuisine Command is a Python command line application for use by a takeaway restaurant.

## Development

### Setting up

I created a GitHub repository from Code Institute's [project template](https://github.com/Code-Institute-Org/p3-template), cloned my repository, and created a virtual environment.

I created a Google Sheets spreadsheet.

I created a Google Cloud project, enabled a Google Drive API, created credentials and a service account, and created a JSON key. I also enabled a Google Sheets API.

I dragged the file of the JSON key into my workspace, renamed it 'creds', copied the client email address from it, shared my spreadsheet to that address, and added 'creds.json' to the gitignore.

I installed gspread and google-auth in my workspace and imported them in the Python script. I pasted in the SCOPE constant, as I had used during Code Institute's "Love Sandwiches" walkthrough project. I used methods of Credentials (from google-auth) and of gspread to give my application access to the external spreadsheet, as demonstrated in the walkthrough project.

### Creating classes

I added 'Name', 'Items ordered', and 'Cost' column headings to my spreadsheet.

I created the MenuItem and Order classes. I defined the confirm method of the Order class. I added temporary dummy instances and a printed method call to test run the script so far, as captured from line 43 onward in my repository's fourth commit (the first commit on Mar 27, 2024).
