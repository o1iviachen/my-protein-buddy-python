import tkinter as tk
import tkinter.messagebox as messagebox
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class HelpPage(tk.Frame):
  """
  Class for help page.

  Attributes
    email_content: tk Text object
        used for user's email content, accessed in other functions
    
  Methods
    authenticate(self, controller, db)
        authenticates the user
    send_email(self, controller):
        send an email to the MyProteinBuddy team
  """

  def __init__(self, parent, controller):
    """
    Initializes HelpPage.

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      parent: tk Frame object
          Container that will hold the frame
    """
    # Inherit from parent class
    tk.Frame.__init__(self, parent)
    self.columnconfigure((0, 1, 2), weight=1)
    # Create all aspects on the page
    description = tk.Label(self,
                           text="Any questions? Email our team!",
                           font=controller.titlefont,
                           bg=controller.BEIGE,
                           fg=controller.BROWN)
    self.email_content = tk.Text(self, height=20, width=25)
    send = tk.Button(self,
                     text="Send email",
                     activebackground=controller.BEIGE2,
                     activeforeground=controller.BROWN,
                     bg=controller.ALMOND,
                     fg=controller.BEIGE,
                     font=controller.titlefont,
                     command=lambda: self.send_email(controller))
    # Grid all aspects onto page
    description.grid(row=0, column=1)
    self.email_content.grid(row=1, column=1)
    send.grid(row=2, column=1, pady=5)

  def send_email(self, controller):
    """
    Send an email to the MyProteinBuddy team (my non-school email).

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
    """
    # Learned how to send mail using https://docs.sendgrid.com/for-developers/sending-email/v3-python-code-example. The following code obtains the email content. If the email content is empty, an error is shown
    body = self.email_content.get('1.0', 'end').rstrip()
    if body != "":
      message = Mail(from_email="olivia63chen@gmail.com",
                     to_emails="olivia63chen@gmail.com",
                     subject='Inquiry about MyProteinBuddy',
                     html_content=f"{body}\nFrom: {controller.user_email}")
      # Tries to send email, but if doesn't work an error is shown
      try:
        sg = SendGridAPIClient(
          api_key=
          "REPLACE_WITH_YOUR_API_KEY"
        )
        # Learned how to clear a text widget using https://www.geeksforgeeks.org/python-tkinter-text-widget/
        self.email_content.delete('1.0', "end")
        sg.send(message)
        messagebox.showinfo(title="Success!", message="The email was sent.")
      except:
        messagebox.showwarning(title="Error",
                               message="The email was not sent.")
    else:
      messagebox.showwarning(title="Error",
                             message="You have not written anything.")
