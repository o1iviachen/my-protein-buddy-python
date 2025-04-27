import tkinter as tk
import tkinter.messagebox as messagebox
import requests
import datetime


class SearchResults(tk.Frame):
  """
  Class for search results page.
  
  Attributes:
    serving_box: tk Entry object
        allows user to input serving amount
    protein: float
        protein amount of food
        
  Methods
    get_information(self, controller, db)
        accesses Nutritionix database to get food data
    write_to_database(self, controller, db)
        write the user's intake to the firestore database
  """

  def __init__(self, parent):
    """
    Initializes SearchResults.

    Args
      parent: tk Frame object
          Container that will hold the frame
    """
    # Inherit from super class
    tk.Frame.__init__(self, parent)
    self.columnconfigure((0, 1, 2), weight=1)
    self.protein = 0
    self.serving_box = None

  def get_information(self, controller, db):
    """
    Gets information from the Nutritionix database.

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Clear frame so information doesn't overlap for previous searches, learned usinghttps://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    for widget in self.winfo_children():
      widget.destroy()
    query = {"query": controller.listing["FoodPage"].food_request}
    # Make a request to Nutrionix. Learned how to using https://stackoverflow.com/questions/63164520/nutritionix-error-messagechild-query-fails-because-query-is-requir
    response = requests.request(
      "POST",
      'https://trackapi.nutritionix.com/v2/natural/nutrients',
      headers={
        'Content-Type': "application/x-www-form-urlencoded",
        'x-app-id': "c1358ca9",
        'x-app-key': "7ecc612b2d7418187f2187710a7da088",
        'x-remote-user-id': "0"
      },
      data=query)
    # Checks if there is an error. If there is, an error is shown
    if "message" in response.json():
      error_label = tk.Label(self,
                             text="Sorry this food is not in the database.",
                             font=controller.titlefont,
                             bg=controller.BEIGE,
                             fg=controller.BROWN)
      return_to_food = tk.Button(
        self,
        text="Return",
        activebackground=controller.BEIGE2,
        activeforeground=controller.BROWN,
        bg=controller.ALMOND,
        fg=controller.BEIGE,
        font=controller.titlefont,
        command=lambda: controller.up_frame("FoodPage"))
      error_label.grid(row=0, column=1)
      return_to_food.grid(row=1, column=1)
    # Parse through json to find protein amount and serving weight and set up new page
    else:
      self.protein = response.json()["foods"][0]["nf_protein"]
      serving_size = response.json()["foods"][0]["serving_weight_grams"]
      # Indicate aforementioned values to user
      protein_label = tk.Label(
        self,
        text=f"The amount of protein: {self.protein} grams",
        font=controller.titlefont,
        bg=controller.BEIGE,
        fg=controller.BROWN)
      size_label = tk.Label(self,
                            text=f"The serving size: {serving_size} grams",
                            font=controller.titlefont,
                            bg=controller.BEIGE,
                            fg=controller.BROWN)
      # Create aspects for input and submission
      serving_question = tk.Label(self,
                                  text="How many servings did you consume?",
                                  font=controller.titlefont,
                                  bg=controller.BEIGE,
                                  fg=controller.BROWN)
      self.serving_box = tk.Entry(self, width=22)
      # Bind return button to submit button
      self.serving_box.bind("<Return>",
                            lambda event, controller=controller, db=db: self.
                            write_to_database(event, controller, db))
      submit_servings = tk.Button(
        self,
        text="Submit",
        activebackground=controller.BEIGE2,
        activeforeground=controller.BROWN,
        bg=controller.ALMOND,
        fg=controller.BEIGE,
        font=controller.titlefont,
        command=lambda: self.write_to_database("", controller, db))
      return_to_food_mistake = tk.Button(
        self,
        text="Return",
        activebackground=controller.BEIGE2,
        activeforeground=controller.BROWN,
        bg=controller.ALMOND,
        fg=controller.BEIGE,
        font=controller.titlefont,
        command=lambda: controller.up_frame("FoodPage"))
      # Set focus on servings box
      self.serving_box.focus_set()
      # Grid all aspects
      protein_label.grid(row=0, column=1, pady=5)
      size_label.grid(row=1, column=1, pady=5)
      serving_question.grid(row=2, column=1, pady=5)
      self.serving_box.grid(row=3, column=1, pady=5)
      submit_servings.grid(row=4, column=1, pady=10)
      return_to_food_mistake.grid(row=5, column=1, pady=10)

  def write_to_database(self, event, controller, db):
    """
    Writes user's protein intake to database 

    Args
      event: Any
          Used to bind return button
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    servings = self.serving_box.get().rstrip()
    num = True
    # Create document
    doc_ref = db.collection('users').document(controller.user_email)
    doc = doc_ref.get()
    # Check is number is a float
    if len(servings) != 0:
      for s in servings:
        if s not in ".1234567890":
          num = False
      # If the number is not a number, an error is shown. If note, the food the written to the database in the today's field with the food name and the protein amount as a key value pair
      if num:
        protein_amount = float("%.2f" % (float(servings) * self.protein))
        today = str(datetime.date.today())
        # Replace all spaces with underscores to conform to firestore format
        food_search = controller.listing["FoodPage"].food_request.replace(
          " ", "_")
        # If there is already a dictionary for today, continue to log food. If not, create a new field
        if today in doc.to_dict():
          # If the food is already in the list, create a new key value pair
          if food_search not in doc.to_dict()[today]:
            doc_ref.update({f'{today}.{food_search}': protein_amount})
          # If is already in the list, add amount to intial value
          else:
            doc_ref.update({
              f'{today}.{food_search}':
              protein_amount + doc.to_dict()[today][food_search]
            })
        else:
          doc_ref.set({today: {}}, merge=True)
          doc_ref.update({f'{today}.{food_search}': protein_amount})
          # Get food for food page, indicating that it is not the initial request
        controller.listing["FoodPage"].get_food(controller, "not", db)
        # Set cursor at food page search box
        controller.listing["FoodPage"].search_box.focus_set()
        controller.up_frame("FoodPage")
      else:
        messagebox.showwarning(title="Error",
                               message="Please enter a valid value.")
    else:
      messagebox.showwarning(title="Error",
                             message="Please enter a valid value.")
      # If the user reached their protein goal and if the goal as not been shown yet, congratulate user and indicate that the goal has already been shown to avoid repeat
    if controller.goal and not controller.goal_shown and controller.starting_intake <= doc.to_dict(
    )["protein_goal"]:
      messagebox.showinfo(title="Congrats",
                          message="You hit your protein goal!")
      controller.goal_shown = True
