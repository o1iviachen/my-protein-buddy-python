import tkinter as tk


class GoalSetter(tk.Frame):
  """
  Class for goal setter page

  Attributes
    slider: tk Scale object
        used to set protein goal
    destination: str
        used to direct user to appropriate page once they choose their protein goal
    
  Methods
    get_information(self, controller, db)
        gets the slider's information and sets up subsequent pages
  """

  def __init__(self, parent, controller, db):
    """
    Initializes GoalSetter.

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      parent: tk Frame object
          Container that will hold the frame
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Inherit from parent class
    tk.Frame.__init__(self, parent)
    self.columnconfigure((0, 1, 2), weight=1)
    # Unless changed, the destination after changing the goal will go to the food page.
    self.destination = "food"
    # Initialize all aspects
    goal = tk.Label(self,
                    text="Set your protein goal in grams: ",
                    font=controller.titlefont,
                    bg=controller.BEIGE,
                    fg=controller.BROWN)
    self.slider = tk.Scale(self,
                           from_=0,
                           to=200,
                           orient="horizontal",
                           length=200)
    submit = tk.Button(self,
                       text="Submit",
                       activebackground=controller.BEIGE2,
                       activeforeground=controller.BROWN,
                       bg=controller.ALMOND,
                       fg=controller.BEIGE,
                       font=controller.titlefont,
                       command=lambda: self.get_information(controller, db))
    # Grid all aspects onto page
    goal.grid(row=0, column=1, pady=5)
    self.slider.grid(row=1, column=1, pady=5)
    submit.grid(row=2, column=1, pady=5)

  def get_information(self, controller, db):
    """
    Gets information for following pages

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Get the slider value
    user_goal = self.slider.get()
    # Update the text showing protein goal and email
    controller.listing["ProfilePage"].user_goal.configure(
      text=f"Current goal: {user_goal}g")
    controller.listing["ProfilePage"].user_email.configure(
      text=f"Current user: {controller.user_email}")
    doc_ref = db.collection('users').document(controller.user_email)
    doc_ref.set({'protein_goal': user_goal}, merge=True)
    # Checks if the user is inputting their protein goal for the first time or not. If they are, they are redirected to the food page. If not, they return to the food page
    if self.destination == "food":
      controller.listing["FoodPage"].create_bar(controller)
      controller.up_frame("FoodPage")
    else:
      controller.up_frame("ProfilePage")
    # Learned how to set the default value using https://stackoverflow.com/questions/3963329/how-can-i-set-the-default-value-of-my-tkinter-scale-widget-slider-to-100
    self.slider.set(0)
