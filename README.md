# Cuisine Command

Cuisine Command is a Python command line application for use by a takeaway restaurant.

## Development

### Consulting mentor

I had a meeting with my Code Institute mentor, Rahul Lakhanpal. Out of four project ideas that I suggested, he advised that the takeaway restaurant ordering system was likely the best option for showing my abilities and for trying to create a product with some potential for real-world application and value. I was inclined to agree.

When I raised the apparent requirement for the project to include classes, he suggested that the menu items and the orders received could be suitable for treatment as classes.

He also mentioned [Ascii Art Generator](https://www.ascii-art-generator.org), [Tabulate](https://pypi.org/project/tabulate), [Colorama](https://pypi.org/project/colorama), and [Cerberus](https://docs.python-cerberus.org), for me to look at and consider making use of.

### Setting up

I created a GitHub repository from Code Institute's [project template](https://github.com/Code-Institute-Org/p3-template), cloned my repository, and created a virtual environment.

I created a Google Sheets spreadsheet.

I created a Google Cloud project, enabled a Google Drive API, created credentials and a service account, and created a JSON key. I also enabled a Google Sheets API.

I dragged the file of the JSON key into my workspace, renamed it 'creds', copied the client email address from it, shared my spreadsheet to that address, and added 'creds.json' to the gitignore.

I installed gspread and google-auth in my workspace and imported them in the Python script. I pasted in the SCOPE constant, as I had used during Code Institute's "Love Sandwiches" walkthrough project. I used methods of Credentials (from google-auth) and of gspread to give my application access to the external spreadsheet, as demonstrated in the walkthrough project.

After the commit, I realised that I had supplied an incorrect name of the spreadsheet to be opened, but it was easily edited and recommitted.

### Creating classes

I added 'Name', 'Items ordered', and 'Cost' column headings to my spreadsheet.

I created the MenuItem and Order classes. I defined the confirm method of the Order class. I added temporary dummy instances and a printed method call to test run the script so far, as captured from line 43 onward in my repository's fourth commit (the first commit on Mar 27, 2024).

### ~~Creating instances~~ Adding menu.py

I had created multiple instances of the MenuItem class. For realism and convenience, I based my foods and prices on a menu leaflet from a local takeaway restaurant.

<img src="screencaps/mi-instances.webp" alt="instances of MenuItem class" width="750px">

(This screen capture was taken with VS Code's CodeSnap extension, published by adpyke.)

However, I then had a couple of ideas that would impact the development of my project:

- I questioned whether creating a huge number of instances when `run.py` first runs is the best approach, or whether dictionaries would be more suitable for the menu.

- It occurred to me that it should be possible to put the menu in a separate Python file and import it, avoiding cluttering up the main script.

I experimented by adding Meal A and Meal B as a dictionary of dictionaries, followed by a temporary

`print(menu_items['Meal A']['foods'][0])`

and then ran the script. As predicted, the terminal printed 'Sweet & Sour Chicken'. I then created `menu.py` , moved the dictionary into it, added an import at the top of `run.py` , and ran it again. It still worked, confirming that an imported dictionary should be a viable approach. At this point, the MenuItem class could be deleted.

I made an adjustment to the for loop in Order's confirm method to account for this new situation, replacing the dot notation with square brackets - very similar to my experiment above.

At this time, I also created a 'screencaps' folder, solely for screen captures included in this README. All images will have been optimized with [Tiny PNG](https://tinypng.com).
