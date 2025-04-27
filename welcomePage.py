import tkinter as tk


class WelcomePage(tk.Frame):
  """ Class for welcome page. """

  def __init__(self, parent, controller):
    """
    Initializes WelcomePage.

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      parent: tk Frame object
          Container that will hold the frame
    """
    # Inherit from super class
    tk.Frame.__init__(self, parent)
    # Learned how to centralize widgets using https://stackoverflow.com/questions/52581748/grid-isnt-centering-my-widget-by-default-in-tkinter-python
    self.columnconfigure((0, 1, 2), weight=1)
    self.rowconfigure((0, 1, 2, 3), weight=1)
    # Create labels, buttons and canva for page
    app_name = tk.Label(self,
                        text="Welcome to\nMyProteinBuddy!",
                        font=controller.titlefont,
                        bg=controller.BEIGE,
                        fg=controller.BROWN)
    canvas = tk.Canvas(self,
                       width=200,
                       height=200,
                       bg=controller.BEIGE,
                       highlightthickness=0)
    sign_up = tk.Button(self,
                        text="Sign up",
                        activebackground=controller.BEIGE2,
                        activeforeground=controller.BROWN,
                        bg=controller.ALMOND,
                        fg=controller.BEIGE,
                        font=controller.titlefont,
                        command=lambda: controller.up_frame("EmailPassSignUp"))
    log_in = tk.Button(self,
                       text="Log in",
                       activebackground=controller.BEIGE2,
                       activeforeground=controller.BROWN,
                       bg=controller.ALMOND,
                       fg=controller.BEIGE,
                       font=controller.titlefont,
                       command=lambda: controller.up_frame("EmailPassLogIn"))
    canvas.create_image(100, 100, image=controller.bao)
    # Grid all aspects
    app_name.grid(row=1, column=1)
    sign_up.grid(row=2, column=1)
    log_in.grid(row=3, column=1)
    canvas.grid(row=4, column=1)
