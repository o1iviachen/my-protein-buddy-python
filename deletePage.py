import tkinter as tk
from firebase_admin import firestore
import tkinter.messagebox as messagebox
import datetime


class DeletePage(tk.Frame):
  """
  Class for delete page in app.

  Attributes
    food_list: tkinter Listbox object
        stores the user's food list
    
  Methods
    return_to_food(self, controller, db)
        resets data and returns to food page
    get_food(self, controller, db)
        gets the food for the delete page as soon as user_email is defined
    delete_food(self, controller, db)
        deletes food from interface and from database
  """

  def __init__(self, parent, controller, db):
    """ 
    Initializes DeletePage
    
    Args:
      parent: Frame object
          Used to create starting container for all frames
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Inherit from super class
    tk.Frame.__init__(self, parent)
    self.columnconfigure((0, 1, 2), weight=1)
    # Create list demonstrating food intake
    self.food_list = tk.Listbox(self,
                                bg=controller.BEIGE,
                                fg=controller.BROWN,
                                font=controller.titlefont,
                                selectbackground=controller.ALMOND,
                                highlightthickness=0,
                                highlightcolor=controller.BEIGE,
                                selectmode=tk.MULTIPLE,
                                width=20,
                                height=8)
    # Create button with function to return to food page
    return_to_food = tk.Button(
      self,
      text="Return to food page",
      activebackground=controller.BEIGE2,
      activeforeground=controller.BROWN,
      bg=controller.ALMOND,
      fg=controller.BEIGE,
      font=controller.titlefont,
      width=15,
      command=lambda: self.return_to_food(controller, db))
    # Create button with function to delete food
    delete = tk.Button(self,
                       text="Delete selected food",
                       activebackground=controller.BEIGE2,
                       activeforeground=controller.BROWN,
                       bg=controller.ALMOND,
                       fg=controller.BEIGE,
                       font=controller.titlefont,
                       width=15,
                       command=lambda: self.delete_food(controller, db))
    # Grid aspects onto application
    self.food_list.grid(row=0, column=1, pady=5)
    delete.grid(row=1, column=1, pady=5)
    return_to_food.grid(row=2, column=1, pady=5)

  def get_food(self, controller, db):
    """
    Initializes and updates the food menu 
    
    Args:
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information
    """
    doc_ref = db.collection('users').document(controller.user_email)
    doc = doc_ref.get()
    today = str(datetime.date.today())
    # Empty food list before adding other items
    self.food_list.delete(0, "end")
    # For food in today, add the food to the list
    if today in doc.to_dict():
      for food in doc.to_dict()[today]:
        if food != "total_intake":
          self.food_list.insert(
            "end", f"{food.replace('_', ' ')}: {doc.to_dict()[today][food]}")

  def delete_food(self, controller, db):
    """
    Deletes food from user's intake 
    
    Args:
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information
    """
    today = str(datetime.date.today())
    doc_ref = db.collection("users").document(controller.user_email)
    # Learned to access selected row using https://www.geeksforgeeks.org/how-to-get-selected-value-from-listbox-in-tkinter/. For each selection, the food is deleted from the food list and eliminated from the database
    # Checks if the user has selected their food
    if len(self.food_list.curselection()) != 0:
      # As the list will shift up for each food deleted, continuously delete the food at that index.
      mutable_food_list = list(self.food_list.curselection())
      for i in mutable_food_list:
        food = self.food_list.get(i).split(": ")[0]
        doc_ref.update(
          {f"{today}.{food.replace(' ', '_')}": firestore.DELETE_FIELD})
        self.food_list.delete(i)
        # Shift all values up one as one is deleted
        for i in range(len(mutable_food_list)):
          # i-1 as lists begin at 0
          mutable_food_list[i - 1] = mutable_food_list[i - 1] - 1
    else:
      messagebox.showwarning(title="Error", message="Please select a food.")

  def return_to_food(self, controller, db):
    """
    Updates food page then returns to food page
    
    Args:
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information
    """
    # Update food page before user can access it
    controller.listing["FoodPage"].get_food(controller, "not", db)
    controller.up_frame("FoodPage")
