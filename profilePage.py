import tkinter as tk


class ProfilePage(tk.Frame):
  """
  Class for profile page.

  Attributes
    user_email: tk Label object
        shows user's email
    user_goal: tk Label object
        shows user's protein goal
    
  Methods
    get_intake(self, controller, db)
        get information after updates
    log_out(self, controller)
        log out from application
    goal_setting(self, controller):
        set up destination for goal setter
  """

  def __init__(self, parent, controller, db):
    """
    Initializes ProfilePage.

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
    # Create aspects for page
    self.user_email = tk.Label(self,
                               text="Current user: ",
                               font=controller.titlefont,
                               bg=controller.BEIGE,
                               fg=controller.BROWN)
    self.user_goal = tk.Label(self,
                              text="Protein goal: ",
                              font=controller.titlefont,
                              bg=controller.BEIGE,
                              fg=controller.BROWN)
    change_protein = tk.Button(self,
                               text="Change protein goal",
                               activebackground=controller.BEIGE2,
                               activeforeground=controller.BROWN,
                               bg=controller.ALMOND,
                               fg=controller.BEIGE,
                               font=controller.titlefont,
                               command=lambda: self.goal_setting(controller))
    change_password = tk.Button(
      self,
      text="Change password",
      activebackground=controller.BEIGE2,
      activeforeground=controller.BROWN,
      bg=controller.ALMOND,
      fg=controller.BEIGE,
      font=controller.titlefont,
      command=lambda: controller.up_frame("PasswordChange"))
    logout = tk.Button(self,
                       text="Log out",
                       activebackground=controller.BEIGE2,
                       activeforeground=controller.BROWN,
                       bg=controller.ALMOND,
                       fg=controller.BEIGE,
                       font=controller.titlefont,
                       command=lambda: self.log_out(controller))
    # Grid aspects onto application
    self.user_email.grid(column=1, row=0, pady=5)
    self.user_goal.grid(column=1, row=1, pady=5)
    change_protein.grid(column=1, row=2, pady=5)
    change_password.grid(column=1, row=3, pady=5)
    logout.grid(column=1, row=4, pady=5)

  def goal_setting(self, controller):
    """
    Set up destination for goal setter

    Args:
      controller: tk Tk object
        used to access main frame 
    """
    controller.listing["GoalSetter"].destination = "profile"
    controller.up_frame("GoalSetter")

  def get_intake(self, controller, db):
    """
    Gets user protein intake goal and email for profile page

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    doc_ref = db.collection('users').document(controller.user_email)
    doc = doc_ref.get()
    # Obtain protein goal from firestore
    self.user_goal.configure(
      text=f"Protein goal: {doc.to_dict()['protein_goal']}g")
    self.user_email.configure(text=f"Current user: {controller.user_email}")

  def log_out(self, controller):
    """
    Logs out from application

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
    """
    # Empties food list
    controller.listing["FoodPage"].mylist.delete(0, "end")
    controller.listing["FoodPage"].intake.configure(
      text="Today's intake: 0.00g")
    controller.listing["GoalSetter"].destination = "food"
    # Delete menu bar
    controller.config(menu="")
    # Clear user.txt as the user is not longer logged in
    open("user.txt", "w").close()
    controller.up_frame("WelcomePage")
