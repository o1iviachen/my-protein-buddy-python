import tkinter as tk
import datetime
import tkinter.messagebox as messagebox


class FoodPage(tk.Frame):
  """
  Class for food page.

  Attributes
    food_request: string
        used across functions to access user's food request
    mylist: tk Listbox object
        shows user's intake 
    search_box: tk Entry object
        input area for user's food request
    intake: tk Label object
        used to show protein intake
    
  Methods
    create_bar(self, controller)
        creates menu bar at top of application
    search(self, controller, db)
        searches for food from Nutrionix database
    get_food(self, controller, initial, db)
        create or update food list shown on food page
    to_delete(self, controller)
        checks if user has food to delete. If so, they proceed to the delete page.
    clear_before_change(self, controller, page)
        clears pages before changing pages
  """

  def __init__(self, parent, controller, db):
    """
    Initializes FoodPage.

    Args
      parent: tk Frame object
          Container that will hold the frame
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Inherit from super class
    tk.Frame.__init__(self, parent)
    self.columnconfigure((0, 1, 2), weight=1)
    self.food_request = ""
    # Initialize aspects that will appear onto the screen
    self.mylist = tk.Listbox(self,
                             bg=controller.BEIGE,
                             fg=controller.BROWN,
                             font=controller.titlefont,
                             selectbackground=controller.ALMOND,
                             highlightthickness=0,
                             highlightcolor=controller.BEIGE,
                             width=20,
                             height=7)
    canvas = tk.Canvas(self,
                       width=100,
                       height=100,
                       bg=controller.BEIGE,
                       highlightthickness=0)
    bao = controller.bao
    canvas.create_image(50, 50, image=bao)
    self.search_box = tk.Entry(self, width=22)
    self.search_box.bind("<Return>",
                         lambda event, controller=controller, db=db: self.
                         search(event, controller, db))
    search_box_descriptor = tk.Label(
      self,
      text="Search for a food to add to your intake:",
      font=controller.titlefont,
      bg=controller.BEIGE,
      fg=controller.BROWN)
    self.intake = tk.Label(self,
                           text="Today's intake: 0.00g",
                           font=controller.titlefont,
                           bg=controller.BEIGE,
                           fg=controller.BROWN)
    search_button = tk.Button(self,
                              text="Search",
                              activebackground=controller.BEIGE2,
                              activeforeground=controller.BROWN,
                              bg=controller.ALMOND,
                              fg=controller.BEIGE,
                              font=controller.titlefont,
                              command=lambda: self.search("", controller, db))
    delete_food = tk.Button(self,
                            text="Delete a food",
                            activebackground=controller.BEIGE2,
                            activeforeground=controller.BROWN,
                            bg=controller.ALMOND,
                            fg=controller.BEIGE,
                            font=controller.titlefont,
                            command=lambda: self.to_delete(controller))
    # Grid all aspects onto page
    canvas.grid(row=0, column=1)
    search_box_descriptor.grid(row=1, column=1, pady=2)
    self.search_box.grid(row=2, column=1, pady=2)
    search_button.grid(row=3, column=1, pady=2)
    self.intake.grid(row=4, column=1, pady=2)
    self.mylist.grid(row=5, column=1, pady=2)
    delete_food.grid(row=6, column=1, pady=2)

  def create_bar(self, controller):
    """
    Creates menu bar for application
    
    Args:
      controller: Tk object
          Used to allow page changes and to access 
    """

    # Create menu bar, learned from https://pythonspot.com/tk-menubar/
    menubar = tk.Menu(controller,
                      background=controller.ALMOND,
                      fg=controller.BEIGE)
    file_menu = tk.Menu(menubar,
                        tearoff=0,
                        background=controller.ALMOND,
                        fg=controller.BEIGE)
    # Add various paths to cascade
    file_menu.add_command(
      label="Food Page",
      command=lambda: self.clear_before_change(controller, "FoodPage"))
    file_menu.add_command(
      label="Stats Page",
      command=lambda: self.clear_before_change(controller, "StatsPage"))
    file_menu.add_command(
      label="Profile Page",
      command=lambda: self.clear_before_change(controller, "ProfilePage"))
    file_menu.add_command(
      label="Help Page",
      command=lambda: self.clear_before_change(controller, "HelpPage"))
    # Make cascade show up on menu
    menubar.add_cascade(menu=file_menu, label="Pages")
    controller.config(menu=menubar)

  def clear_before_change(self, controller, page):
    """
    Clears pages before changing pages.

    Args:
      controller: tk Tk object
          used to access main frame 
      page: string
          used to go to requested page
    """
    # Reset slider to 0
    controller.listing["GoalSetter"].slider.set(0)
    # Clear various text boxes
    controller.listing["HelpPage"].email_content.delete('1.0', "end")
    controller.listing["PasswordChange"].new_password_box.delete(0, "end")
    controller.listing["PasswordChange"].current_password_box.delete(0, "end")
    controller.listing["FoodPage"].search_box.delete(0, "end")
    # Set cursor at search box if going to food page
    if page == "FoodPage":
      controller.listing["FoodPage"].search_box.focus_set()
    controller.up_frame(page)

  def search(self, event, controller, db):
    """
    Initiates search process for foods.
    
    Args:
      event: Any
          to bind return to this function
      controller: Tk object
          Used to allow page changes and to access 
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Obtain food search from user's input
    self.food_request = self.search_box.get().rstrip()
    # If user's input is empty, error is shown. Otherwise, search box is cleared and user is directed to search results.
    if len(self.food_request) == 0:
      messagebox.showwarning(title="Error", message="Please input a food")
    else:
      controller.listing["SearchResults"].get_information(controller, db)
      controller.up_frame("SearchResults")
      self.search_box.delete(0, "end")

  def to_delete(self, controller):
    """
    Directs user to delete page if they have food to delete
    
    Args:
      controller: Tk object
          Used to allow page changes and to access  
    """
    # Learned how to check the list of a tk Listbox object using https://stackoverflow.com/questions/46582151/python-3-getting-amount-of-items-in-listbox-widget. If the user has not inputted any foods for today, they are not directed to the delete page.
    if self.mylist.size() == 0:
      messagebox.showwarning(title="Error", message="Your intake is empty")
    else:
      controller.up_frame("DeletePage")

  def get_food(self, controller, initial, db):
    """
    Get food for list on page.
    
    Args:
      controller: Tk object
          Used to allow page changes and to access 
      initial: str
          used to determine the starting intake if the user just logged in  
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Obtain information from user
    doc_ref = db.collection('users').document(controller.user_email)
    doc = doc_ref.get()
    today = str(datetime.date.today())
    # Clear current list
    self.mylist.delete(0, "end")
    today_intake = 0
    # If user already logged in today, they obtain their current intake. If not, a new field is initialized
    if today in doc.to_dict():
      for food in doc.to_dict()[today]:
        if food != "total_intake":
          # Convert all underscores to spaces to make words from firestore-friendly to user friendly
          self.mylist.insert(
            "end", f"{food.replace('_', ' ')}: {doc.to_dict()[today][food]}")
          # The intake amount increases too
          today_intake += float(doc.to_dict()[today][food])
      doc_ref.update({f'{today}.{"total_intake"}': today_intake})
      # Learned how to format a float using https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points and configure text label using https://www.tutorialspoint.com/changing-tkinter-label-text-dynamically-using-label-configure. Changed the float because sometimes it goes into infinite decimal value.
      self.intake.configure(text=f"Today's intake: {'%.2f' % today_intake}g")
      # Update delete page as well
      controller.listing["DeletePage"].get_food(controller, db)
      # When the user first logs in, it gets the starting intake to make sure to avoid repeating celebratory statements indicating that the user reached their goal
      if initial == "initial":
        controller.starting_intake = today_intake
    else:
      doc_ref.set({today: {}}, merge=True)
    # If the intake is larger than the user's protein goal, mark that the user has reached their goal
    if today_intake > doc_ref.get().to_dict()["protein_goal"]:
      controller.goal = True
