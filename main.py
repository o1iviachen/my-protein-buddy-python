"""
MyProteinBuddy
Olivia Chen
ICS3U

This program looks to provide a protein-tracking application prototype.

History:
08/04/23: Started coding, switched from Kivy (initially switched from Flutter)
11/05/23 Finished coding, began debugging
04/06/23 Project completion
"""

import tkinter as tk
import tkinter.font as font
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import datetime

from deletePage import DeletePage
from emailPassLogIn import EmailPassLogIn
from emailPassSignUp import EmailPassSignUp
from foodPage import FoodPage
from goalSetter import GoalSetter
from helpPage import HelpPage
from passwordChange import PasswordChange
from searchResults import SearchResults
from welcomePage import WelcomePage
from statsPage import StatsPage
from profilePage import ProfilePage

# Initialize firestore with credentials
cred = credentials.Certificate(
  'python-te-98768-firebase-adminsdk-8xjdc-839fb11e0e.json')
firebase_admin.initialize_app(cred)


class MainFrame(tk.Tk):
  """
  Class for main frame or window in application. Controls other pages in the application

  Attributes
    titlefont: tk Font object
        font accessed across the application
    BEIGE2: str
        colour constant accessed across the application
    BEIGE: str
        colour constant accessed across the application
    BROWN: str
        colour constant accessed across the application
    ALMOND: str
        colour constant accessed across the application
    goal: Boolean
        indicates if food goal has been met
    goal_shown: Boolean
        indicates if food goal celebration has been shown
    starting_intake: float
        used to check if user has already reached their protein goal in previous log ins
    listing: dict
        used to transition between pages
    user_email: string
        used to access user's database throughout the code
    bao: tk PhotoImage object
        image asset used across the application
        
  Methods
    up_frame(self, page_name)
        allows the application to change frames or pages
    get_information(self, db)
        allows application to get all necessary information if user is already logged in
  """

  def __init__(self, *args, **kwargs):
    """ Initializes MainFrame """
    # Inherit from parent class
    tk.Tk.__init__(self, *args, **kwargs)
    # Initialize all attributes that will be used throughout the application
    self.titlefont = font.Font(family="Times", size=10)
    self.BEIGE2 = "#D9B382"
    self.BEIGE = "#fff0db"
    self.BROWN = "#663300"
    self.ALMOND = "#AB784E"
    self.search = ""
    self.goal = False
    self.goal_shown = False
    self.starting_intake = 0
    self.listing = {}
    self.user_email = ""
    self.bao = tk.PhotoImage(file="little_mascot.gif")
    # Initialize firestore database
    db = firestore.client()
    # As the logged in user's email is in the text file, check if an individual is logged in by checking if the file is empty or not, learned from https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
    if os.stat("user.txt").st_size != 0:
      # If the user is logged in, change the user email to email in text file
      with open("user.txt", "r+") as file:
        self.user_email = file.read()
    # Initialize the container and its characteristics
    container = tk.Frame()
    # Ensure that container covers entire application, learned from  https://stackoverflow.com/questions/52581748/grid-isnt-centering-my-widget-by-default-in-tkinter-python
    container.grid(row=0, column=0, sticky='nesw')
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    # Ensure that controller covers entire application by matching the dimensions
    self.geometry("300x400")
    self.resizable(0, 0)
    self.configure(bg="#fff0db")
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    # Loops through pages to initialize each page. The pages in this for loop need to access the firestore database and controller
    for page in [
        EmailPassSignUp, EmailPassLogIn, GoalSetter, FoodPage, ProfilePage,
        PasswordChange, DeletePage
    ]:
      page_name = page.__name__
      frame = page(parent=container, controller=self, db=db)
      frame.configure(background="#fff0db")
      frame.grid(row=0, column=0, sticky="nesw")
      # Append to listing to later transfer between pages
      self.listing[page_name] = frame
    # Loops through pages to initialize each page. The pages in this for loop do not need to access the firestore database
    for page in [WelcomePage, HelpPage, StatsPage]:
      page_name = page.__name__
      frame = page(parent=container, controller=self)
      frame.configure(background="#fff0db")
      frame.grid(row=0, column=0, sticky="nesw")
      # Append to listing to use to transfer between pages
      self.listing[page_name] = frame
    # Initialize search results page. It doesn't need a database nor a controller
    for page in [SearchResults]:
      page_name = page.__name__
      frame = page(parent=container)
      frame.configure(background="#fff0db")
      frame.grid(row=0, column=0, sticky="nesw")
      self.listing[page_name] = frame
    # If the user is logged in, go to food page. If not, go to welcome page.
    if self.user_email == "":
      self.up_frame('WelcomePage')
    else:
      # Get necessary user information to set up page
      self.get_information(db)
      self.up_frame('FoodPage')

  def up_frame(self, page_name):
    """
    Allows the application to change frames
    
    Args:
      page_name: str
          the page that the user wants to access
    """
    # Gets the page associated with the page name from the listing dictionary
    page = self.listing[page_name]
    page.tkraise()

  def get_information(self, db):
    """
    Allows application to get all necessary information if user is already logged in

    Args:
      db: firestore client object
        used across the code to access database to read and write
    """
    today = str(datetime.date.today())
    doc_ref = db.collection('users').document(self.user_email)
    # Initialize today's dictionary is the user hasn't logged in yet
    if today not in doc_ref.get().to_dict():
      doc_ref.set({today: {"total_intake": 0}}, merge=True)
    # Get food intake for food page, "initial" argument checks if the celebration goal has already been shown when logged in
    self.listing["FoodPage"].get_food(self, "initial", db)
    # Get food intake for delete page
    self.listing["DeletePage"].get_food(self, db)
    # Create navigation bar
    self.listing["FoodPage"].create_bar(self)
    # Create user's intake graph in stats page
    self.listing["StatsPage"].create_graph(self, db)
    # Get food intake for profile page
    self.listing["ProfilePage"].get_intake(self, db)
    # Set cursor to search box at food page
    self.listing["FoodPage"].search_box.focus_set()
    # Go to food page
    self.up_frame("FoodPage")


app = MainFrame()
app.mainloop()
