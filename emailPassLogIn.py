import tkinter as tk
import tkinter.messagebox as messagebox
import datetime


class EmailPassLogIn(tk.Frame):
  """
  Class for email log in page.

  Attributes
    email_box: tk Entry object
        used for user's email, accessed in other functions
    password_box: tk Entry object
        used for user's password, accesses in other functions
    show_hide_pass: tk Button object
        used to change if the user can see password or not
        
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
    Initializes EmailPassLogIn.

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      parent: tk Frame object
          Container that will hold the frame
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
    # Used https://stackoverflow.com/questions/10989819/hiding-password-entry-input-in-python to find out way to hide password
    self.password_box = tk.Entry(self, width=22, show="*")
    self.show_hide_pass = tk.Button(self,
                                    text="Show password",
                                    activebackground=controller.BEIGE2,
                                    activeforeground=controller.BROWN,
                                    bg=controller.ALMOND,
                                    fg=controller.BEIGE,
                                    font=controller.titlefont,
                                    command=lambda: self.show_hide_password())
    login = tk.Button(self,
                      text="Log in",
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
    # Bind enter to email box to go automatically to  password box
    self.email_box.bind("<Return>",
                        lambda event: self.password_box.focus_set())
    # Bind enter to password box to submit automatically
    self.password_box.bind("<Return>",
                           lambda event, controller=controller, db=db: self.
                           authenticate(event, controller, db))
    # Start cursor at email box
    self.email_box.focus_set()
    # Grid aspects onto page
    email.grid(row=0, column=1)
    self.email_box.grid(row=1, column=1)
    password.grid(row=2, column=1)
    self.password_box.grid(row=3, column=1)
    # Learned how to pad items using https://www.reddit.com/r/learnpython/comments/pumip2/tkinter_make_some_space_between_elements/
    self.show_hide_pass.grid(row=4, column=1, pady=5)
    login.grid(row=5, column=1, pady=5)
    back_button.grid(row=6, column=1, pady=5)

  def show_hide_password(self):
    """ Shows or hides the user's password """
    # Learned how to check if the password is showing using https://1bestcsharp.blogspot.com/2022/05/python-tkinter-show-and-hide-password-text.html
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
    
    Args
      event: Any
          Used for return binding
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information
    """
    user_email = self.email_box.get().rstrip()
    # Checks if email has a domain. If it does not have a domain, an error is shown. Cannot have forward slash as to not impede with firestore.
    if len(user_email.split("@")[-1].split(".")) != 2 or "/" in user_email:
      messagebox.showwarning(title="Error", message="Email is invalid")
    else:
      user_password = self.password_box.get().rstrip()
      doc_ref = db.collection('users').document(user_email)
      doc = doc_ref.get()
      # Checks if email is in database. If it isn't, an error is shown
      if doc.exists:
        # Checks if password is correct by comparing user input the password stores in database. If it is not correct, an error is shown. Otherwise, a new dictionary is set for today's intake if the user hasn't logged any food yet. 
        if doc.to_dict()["password"] != user_password:
          messagebox.showwarning(title="Error",
                                 message="Your password is incorrect")
        else:
          today = str(datetime.date.today())
          doc_ref = db.collection('users').document(user_email)
          if today not in doc.to_dict():
            doc_ref.set({today: {"total_intake": 0}}, merge=True)
          controller.user_email = user_email
          # Learned how to clear a entry widget using https://sites.google.com/a/pythonlake.com/django/tkinterentrydelete
          self.email_box.delete(0, "end")
          # Learned how to clear an entry widget using https://sites.google.com/a/pythonlake.com/django/tkinterentrydelete
          self.password_box.delete(0, "end")
          # Write user into text file so that when they log in, they remain logged in unless they choose to log out.
          with open("user.txt", "w") as file:
            file.write(user_email)
          # Get food in food page
          controller.listing["FoodPage"].get_food(controller, "initial", db)
          # Get food in delete page
          controller.listing["DeletePage"].get_food(controller, db)
          # Create bar in food page
          controller.listing["FoodPage"].create_bar(controller)
          # Create graph in stats page
          controller.listing["StatsPage"].create_graph(controller, db)
          # Get necessary information for profile page
          controller.listing["ProfilePage"].get_intake(controller, db)
          # Set cursor in search box at food page
          controller.listing["FoodPage"].search_box.focus_set()
          # Go to food page
          controller.up_frame("FoodPage")
      else:
        messagebox.showwarning(
          title="Error",
          message="Your email is not in our database. Did you mean to sign up?"
        )

  def go_to_welcome(self, controller): 
    """
    Clears values before going to welcome

    Args:
      controller: tk Tk object
        used to access main frame
    """
    # Clear boxes
    self.email_box.delete(0, "end")
    self.password_box.delete(0, "end")
    # Go to welcome page
    controller.up_frame("WelcomePage")
