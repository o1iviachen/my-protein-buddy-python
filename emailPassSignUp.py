import tkinter as tk
import tkinter.messagebox as messagebox
import datetime


class EmailPassSignUp(tk.Frame):
  """
  Class for email sign up page.

  Attributes
    email_box: tk Entry object
        used for user's email, accesses in other functions
    password_box: tk Entry object
        used for user's password, accesses in other functions
    show_hide_pass: tk Button object
        used to change if the user can see
    
  Methods
    authenticate(self, controller, db)
        authenticates the user
    show_hide_password(self)
        shows or hides the user's password
    go_to_welcome(self, event):
        clear boxes before returning to welcome page
  """

  def __init__(self, parent, controller, db):
    """
    Initializes EmailPassSignUp.

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
    # Create labels and input boxes
    email = tk.Label(self,
                     text="Email:",
                     font=controller.titlefont,
                     bg=controller.BEIGE,
                     fg=controller.BROWN)
    self.email_box = tk.Entry(self, width=22)
    password = tk.Label(self,
                        text="Password:",
                        font=controller.titlefont,
                        bg=controller.BEIGE,
                        fg=controller.BROWN)
    self.password_box = tk.Entry(self, width=22, show="*")
    self.show_hide_pass = tk.Button(self,
                                    text="Show password",
                                    activebackground=controller.BEIGE2,
                                    activeforeground=controller.BROWN,
                                    bg=controller.ALMOND,
                                    fg=controller.BEIGE,
                                    font=controller.titlefont,
                                    command=lambda: self.show_hide_password())
    signup = tk.Button(self,
                       text="Sign up",
                       activebackground=controller.BEIGE2,
                       activeforeground=controller.BROWN,
                       bg=controller.ALMOND,
                       fg=controller.BEIGE,
                       font=controller.titlefont,
                       command=lambda: self.authenticate("", controller, db))
    back_button = tk.Button(self,
                            text="Back to welcome page",
                            activebackground=controller.BEIGE2,
                            activeforeground=controller.BROWN,
                            bg=controller.ALMOND,
                            fg=controller.BEIGE,
                            font=controller.titlefont,
                            command=lambda: self.go_to_welcome(controller))
    # Bind enter to email box to go automatically to password box
    self.email_box.bind("<Return>",
                        lambda event: self.password_box.focus_set())
    # Bind enter to password box to submit automatically
    self.password_box.bind("<Return>",
                           lambda event, controller=controller, db=db: self.
                           authenticate(event, controller, db))
    # Start cursor at current password
    self.email_box.focus_set()
    # Grid aspects onto application
    email.grid(row=0, column=1)
    self.email_box.grid(row=1, column=1)
    password.grid(row=2, column=1)
    self.password_box.grid(row=3, column=1)
    self.show_hide_pass.grid(row=4, column=1, pady=5)
    signup.grid(row=5, column=1, pady=5)
    back_button.grid(row=6, column=1, pady=5)

  def show_hide_password(self):
    """
    Shows or hides the user's password
    """
    # If the password box is showing "*", change to show password
    if self.password_box['show'] == '*':
      self.password_box['show'] = ''
      self.show_hide_pass.configure(text="Hide password")
    # If the password box is showing the password, channge to show "*"
    else:
      self.password_box['show'] = '*'
      self.show_hide_pass.configure(text="Show password")

  def authenticate(self, event, controller, db):
    """
    Authenticates the user 
    
    Args:
      event: Any
          Used to bind return
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information
    """
    user_email = self.email_box.get().rstrip()
    # Checks if email has a domain. If it does not have a domain, an error is shown
    if len(user_email.split("@")[-1].split(".")) != 2 or "/" in user_email:
      messagebox.showwarning(title="Error", message="Email is invalid")
    else:
      user_password = self.password_box.get().rstrip()
      # Checks if password is at least 4 characters. If it is not, an error is shown
      if len(user_password) < 4:
        messagebox.showwarning(
          title="Error", message="Password must be at least 4 characters long")
      else:
        doc_ref = db.collection('users').document(user_email)
        doc = doc_ref.get()
        # Checks the database is the email is already registered. If it is, an error is shown indicating to the user that they might want to log in. Otherwise, a new field for the user's intake today is initialized and the email is written to the text file. Pages needed to be set up are set up.
        if doc.exists:
          messagebox.showwarning(
            title="Error",
            message=
            "Your email is already in our database, did you mean to log in?")
        else:
          today = str(datetime.date.today())
          user_json = {
            "password": user_password,
            today: {
              "total_intake": 0
            },
            "protein_goal": 0
          }
          doc_ref = db.collection('users').document(user_email)
          doc_ref.set(user_json)
          controller.user_email = user_email
          # Clear entry widgets
          self.email_box.delete(0, "end")
          self.password_box.delete(0, "end")
          controller.up_frame("GoalSetter")
          # Write the user's email into the file to make sure they stay logged in
          with open("user.txt", "w") as file:
            file.write(user_email)
          # Create graph
          controller.listing["StatsPage"].create_graph(controller, db)

  def go_to_welcome(self, controller):
    """
    Clears values before going to welcome page

    Args:
      controller: tk Tk object
        used to access main frame
    """
    # Clear boxes
    self.email_box.delete(0, "end")
    self.password_box.delete(0, "end")
    # Go to welcome page
    controller.up_frame("WelcomePage")
