import tkinter as tk
import datetime


class StatsPage(tk.Frame):
  """
  Class for stats page.
    
  Methods
    create_graph(self, controller, db)
        creates graph
  """

  def __init__(self, parent, controller):
    """
    Initializes StatsPage.

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      parent: tk Frame object
          Container that will hold the frame
    """
    # Inherit from super class
    tk.Frame.__init__(self, parent)
    self.columnconfigure((0, 1, 2), weight=1)

  def create_graph(self, controller, db):
    """
    Create graph on the application. Not created earlier to avoid empty requests to firebase

    Args
      controller: Tk object
          Used to allow page changes and to access appliction attributes
      db: firestore client object
          Used to access firestore database to persist information 
    """
    # Initialize labels
    label = tk.Label(self,
                     text="Your intake in the last seven days!",
                     font=controller.titlefont,
                     bg=controller.BEIGE,
                     fg=controller.BROWN)
    # Define the graph's width
    graph_width = 240
    graph_height = 350
    graph = tk.Canvas(self,
                      width=graph_width,
                      height=graph_height,
                      bg=controller.BEIGE,
                      highlightthickness=0)
    # Grid aspects onto page
    graph.grid(row=0, column=1)
    label.grid(row=1, column=1)
    doc_ref = db.collection('users').document(controller.user_email)
    doc = doc_ref.get()
    date_list = []
    tracked = True
    days_before = 1
    # Calculates streak by looping through dates until there is no data or no logged food.
    while tracked:
      # Accessed previous days using https://stackoverflow.com/questions/30483977/python-get-yesterdays-date-as-a-string-in-yyyy-mm-dd-format
      date = str(datetime.date.today() - datetime.timedelta(days_before))
      if date not in doc.to_dict():
        days_before -= 1
        tracked = False
      elif doc.to_dict()[date]["total_intake"] == 0:
        days_before -= 1
        tracked = False
      else:
        days_before += 1
    streak_label = tk.Label(self,
                            text=f"You have a {days_before}-day streak!",
                            font=controller.titlefont,
                            bg=controller.BEIGE,
                            fg=controller.BROWN)
    streak_label.grid(row=2, column=1)
    # Get data from the last seven days in reverse (get earlier days first)
    for i in range(1, 8):
      date_list.append(str(datetime.date.today() - datetime.timedelta(9 - i)))
    data = []
    for date in date_list:
      if date in doc.to_dict():
        intake = round(doc.to_dict()[date]["total_intake"], 2)
        data.append(intake)
      # If date is not in database, the day's data is 0
      else:
        data.append(0)
    # Followed #https://stackoverflow.com/questions/35666573/use-tkinter-to-draw-a-specific-bar-chart to create graph
    # The variables below size the bar graph
    y_stretch = 15  # The highest y = max_data_value * y_stretch
    y_gap = 20  # The gap between lower canvas edge and x axis
    x_stretch = 10  # Stretch x wide enough to fit the variables
    x_width = 20  # The width of the x-axis
    x_gap = 20  # The gap between left canvas edge and y axis
    # For loop to calculate the rectangle
    for x, y in enumerate(data):
      # coordinates of each bar
      # Bottom left coordinate
      x0 = x * x_stretch + x * x_width + x_gap
      # Top left coordinates
      y0 = graph_height - (y / 10 * y_stretch + y_gap)
      # Bottom right coordinates
      x1 = x * x_stretch + x * x_width + x_width + x_gap
      # Top right coordinates
      y1 = graph_height - y_gap
      # Draw the bar
      graph.create_rectangle(x0, y0, x1, y1, fill=controller.BROWN)
      # Put the y value above the bar
      graph.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y))
