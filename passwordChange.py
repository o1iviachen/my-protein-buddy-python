import tkinter as tk
import tkinter.messagebox as messagebox


class PasswordChange(tk.Frame):
  """
  Class for password change page.

  Attributes
    current_password_box: tk Entry object
        used to access user's input for current password, accessed in other functions
    new_password_box: tk Entry object
        used to access user's input for new password, accessed in other functions
    show_hide_pass: tk Button object
        used to allow user to show or hide password
    
  Methods
    verify_password(self, controller, db)
        verify if user is allowed to change password
    go_to_profile(self, controller)
        resets profile page before going to profile page
    show_hide_password(self):
        shows or hides password
  """

  def __init__(self, parent, controller, db):
    """
    Initializes PasswordChange.

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
    # Create aspects of page
    current_password = tk.Label(self,
                                text="Enter your current password:",
                                font=controller.titlefont,
                                bg=controller.BEIGE,
                                fg=controller.BROWN)
    self.current_password_box = tk.Entry(self, width=22, show="*")
    new_password = tk.Label(self,
                            text="Enter your new password:",
                            font=controller.titlefont,
                            bg=controller.BEIGE,
                            fg=controller.BROWN)
    self.show_hide_pass = tk.Button(self,
                                    text="Show passwords",
                                    activebackground=controller.BEIGE2,
                                    activeforeground=controller.BROWN,
                                    bg=controller.ALMOND,
                                    fg=controller.BEIGE,
                                    font=controller.titlefont,
                                    command=lambda: self.show_hide_password())
    submit = tk.Button(
      self,
      text="Submit",
      activebackground=controller.BEIGE2,
      activeforeground=controller.BROWN,
      bg=controller.ALMOND,
      fg=controller.BEIGE,
      font=controller.titlefont,
      command=lambda: self.verify_password("", controller, db))
    back_button = tk.Button(self,
                            text="Back to profile page",
                            activebackground=controller.BEIGE2,
                            activeforeground=controller.BROWN,
                            bg=controller.ALMOND,
                            fg=controller.BEIGE,
                            font=controller.titlefont,
                            command=lambda: self.go_to_profile(controller))
    self.new_password_box = tk.Entry(self, width=22, show="*")
    # Bind enter to current password box to go automatically to new password box
    self.current_password_box.bind(
      "<Return>", lambda event: self.new_password_box.focus_set())
    # Bind enter to new password box to submit automatically
    self.new_password_box.bind("<Return>",
                               lambda event, controller=controller, db=db: self
                               .verify_password(event, controller, db))
    # Grid items onto page
    current_password.grid(row=0, column=1, pady=5)
    self.current_password_box.grid(row=1, column=1, pady=5)
    new_password.grid(row=2, column=1, pady=5)
    self.new_password_box.grid(row=3, column=1, pady=5)
    self.show_hide_pass.grid(row=4, column=1, pady=5)
    submit.grid(row=5, column=1, pady=5)
    back_button.grid(row=6, column=1, pady=5)

  def show_hide_password(self):
    """ Shows or hides the user's password """
    # Learned how to check if the password is showing using https://1bestcsharp.blogspot.com/2022/05/python-tkinter-show-and-hide-password-text.html
    if self.new_password_box['show'] == '*':
      self.new_password_box['show'] = ''
      self.current_password_box['show'] = ''
      self.show_hide_pass.configure(text="Hide passwords")
    else:
      self.new_password_box['show'] = '*'
      self.current_password_box['show'] = '*'
      self.show_hide_pass.configure(text="Show passwords")

  def verify_password(self, event, controller, db):
    """
    Verifies if user has inputted their old password correctly to change their new password

    Args
      event: Any
          Used to bind return to function
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    doc_ref = db.collection('users').document(controller.user_email)
    # Obtains user's input for their old password
    user_current_pass = self.current_password_box.get().rstrip()
    # Obtains user's input for their new password
    user_new_pass = self.new_password_box.get().rstrip()
    # If the old password is equivalent to the current password in the password field in the firestore database, the program checks the new password. Otherwise, an error is shown
    if user_current_pass == doc_ref.get().to_dict()["password"]:
      # If the new pass is less than 4 characters, an error is shown
      if len(user_new_pass) < 4:
        messagebox.showwarning(
          title="Error",
          message="The new password should at least 4 characters")
      # If they reuse a a password, an error is shown
      elif user_new_pass == user_current_pass:
        messagebox.showwarning(title="Error",
                               message="You must use a new password")
      # If they fulfill all password criterias, the password is changed
      else:
        doc_ref.set({"password": user_new_pass}, merge=True)
        self.current_password_box.delete(0, "end")
        self.new_password_box.delete(0, "end")
        controller.up_frame("ProfilePage")
    else:
      messagebox.showwarning(title="Error",
                             message="The current password is incorrect.")

  def go_to_profile(self, controller):
    """
    Resets profile page and goes to profile page

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
    """
    # Clear password boxes
    self.current_password_box.delete(0, "end")
    self.new_password_box.delete(0, "end")
    controller.up_frame("ProfilePage")
