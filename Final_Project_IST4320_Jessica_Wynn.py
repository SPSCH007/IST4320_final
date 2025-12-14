#!/usr/bin/env python
# coding: utf-8

# In[20]:


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import pandas as pd
import sqlite3

import sv_ttk

# Initializing tkinter
main = tk.Tk()
main.title("Card Game: War")
main.geometry('1200x800')
main.resizable(False, False)

def clear_widgets(frame):
    '''
    Clears the widgets of each active frame 
    prior to opening new widgets to prevent duplication
    '''
    for widget in frame.winfo_children():
        widget.destroy()
        
# Main Menu
def load_frame1(): 
    clear_widgets(frame2) # Clear all frame 2 widgets
    clear_widgets(frame3) # Clear all frame 3 widgets
    frame1.tkraise() # Raise frame 1 to display
    frame1.pack_propagate(False) 
    '''
    Load the main menu
    1. Load the image
    2. Display the title
    3. Display the play button
    4. Display the stats button
    5. Display the quit button
    6. Display the toggle theme button
    '''
    
    # Header image
    card_img = Image.open("PNG-cards-1.3/ace_of_spades.png").resize((250, 363))
    card_img_tk = ImageTk.PhotoImage(card_img)
    card_label = tk.Label(frame1, image = card_img_tk)
    card_label.image = card_img_tk
    card_label.pack(pady = 20)
    
    # Header Title
    header_label = tk.Label(frame1,
                            text = "Card Game: War",
                            font = ("TkMenuFont", 20)
    )
    header_label.pack()
    
    # Button Play
    play_button = tk.Button(
        frame1,
        text = "Play",
        font = ("TkHeadingFont", 15),
        command = lambda:load_frame2()
        )
    play_button.pack(pady=10)
    
    # Button Stats
    stats_button = tk.Button(
        frame1,
        text = "Stats",
        font = ("TkHeadingFont", 15),
        command = lambda:load_frame3()
        )
    stats_button.pack(pady=10)
    
    # Button Quit
    quit_button = tk.Button(
        frame1,
        text = "Quit",
        font = ("TkHeadingFont", 15),
        command = lambda:main.destroy()
        )
    quit_button.pack(pady=10)
    
    
    # Sets the default theme to dark mode
    sv_ttk.set_theme("dark")
    
    # Toggles the theme between light/dark mode
    theme_button = ttk.Button(frame1, text="Toggle Dark/Light Mode", command=sv_ttk.toggle_theme)
    theme_button.pack(pady=25)

# Game Screen
def load_frame2():
    clear_widgets(frame2) # Clear all prior frame2 widgets (for repeated game use)
    clear_widgets(frame1) # Clear main menu widgets
    frame2.tkraise() # Raise frame 2 to display
    game()

    # Button Fight
    fight_button = tk.Button(
        frame2,
        text = "Fight",
        font = ("TkHeadingFont", 15),
        command = lambda:load_frame2()
        )
    fight_button.pack(pady=10)
    
    # Button Back
    back_button = tk.Button(
        frame2,
        text = "Back",
        font = ("TkHeadingFont", 15),
        command = lambda:load_frame1()
        )
    back_button.pack(pady=10)
    
def game():
    '''
    1. Initialize the enemy card image and value variables
    2. Call the set_card function to pull a random card
    3. Repeat step 1 and 2 for the user's card
    4. Display the cards using labels
    5. Compare the values of the enemy and user's cards
    6. Store the results in SQL
    '''
    enemy_card, enemy_card_value = set_card()
    your_card, your_card_value = set_card()

    # Enemy card display
    enemy_img = Image.open(enemy_card).resize((125, 182))
    enemy_img_tk = ImageTk.PhotoImage(enemy_img)
    enemy_card_label = tk.Label(frame2, image = enemy_img_tk)
    enemy_card_label.image = enemy_img_tk
    enemy_card_label.pack(pady = 20)
    
    # Your card display
    your_img = Image.open(your_card).resize((125, 182))
    your_img_tk = ImageTk.PhotoImage(your_img)
    your_card_label = tk.Label(frame2, image = your_img_tk)
    your_card_label.image = your_img_tk
    your_card_label.pack(pady = 20)

    # Display win/loss
    result = ""
    if enemy_card_value > your_card_value: # Enemy has a higher value card
        result = "Loss"
    elif your_card_value > enemy_card_value: # Player has a higher value card
        result = "Win"
    else: # Both cards are even
        result = "Tie"
    stats(result) # Record the result

    # Display win status
    status_label = tk.Label(frame2,
                            text = result,
                            font = ("TkMenuFont", 20)
    )
    status_label.pack()

def stats(result):
    '''
    1. Create a SQLite database named stat.db
    2. Ensure that the proper table is created if doesn't exist
    3. Insert the result of the game into a new row of the table
    '''
    # Create a SQLite database
    sql_connect = sqlite3.connect('stat.db')
    cursor = sql_connect.cursor() 
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS statistics (
        game INTEGER PRIMARY KEY AUTOINCREMENT,
        result VARCHAR(32)
        )
    ''')
    sql_connect.commit()
    
    # Saving the data into the database through a query
    query = "INSERT INTO statistics(game, result) VALUES (NULL, ?)"
    cursor.execute(query, (result,))
    sql_connect.commit()
    
def set_card():
    '''
    1. Pull a random key/value from the deck dictionary
    2. Split into a card for indexing the image
    3. Split into a card value for comparing if user won or not
    '''
    card = ''
    card_value = 0
    deck = {
        "PNG-cards-1.3/2_of_clubs.png" : 2,
        "PNG-cards-1.3/2_of_diamonds.png" : 2,
        "PNG-cards-1.3/2_of_hearts.png" : 2,
        "PNG-cards-1.3/2_of_spades.png" : 2,
        "PNG-cards-1.3/3_of_clubs.png" : 3,
        "PNG-cards-1.3/3_of_diamonds.png" : 3,
        "PNG-cards-1.3/3_of_hearts.png" : 3,
        "PNG-cards-1.3/3_of_spades.png" : 3,
        "PNG-cards-1.3/4_of_clubs.png" : 4,
        "PNG-cards-1.3/4_of_diamonds.png" : 4,
        "PNG-cards-1.3/4_of_hearts.png" : 4,
        "PNG-cards-1.3/4_of_spades.png" : 4,
        "PNG-cards-1.3/5_of_clubs.png" : 5,
        "PNG-cards-1.3/5_of_diamonds.png" : 5,
        "PNG-cards-1.3/5_of_hearts.png" : 5,
        "PNG-cards-1.3/5_of_spades.png" : 5,
        "PNG-cards-1.3/6_of_clubs.png" : 6,
        "PNG-cards-1.3/6_of_diamonds.png" : 6,
        "PNG-cards-1.3/6_of_hearts.png" : 6,
        "PNG-cards-1.3/6_of_spades.png" : 6,
        "PNG-cards-1.3/7_of_clubs.png" : 7,
        "PNG-cards-1.3/7_of_diamonds.png" : 7,
        "PNG-cards-1.3/7_of_hearts.png" : 7,
        "PNG-cards-1.3/7_of_spades.png" : 7,
        "PNG-cards-1.3/8_of_clubs.png" : 8,
        "PNG-cards-1.3/8_of_diamonds.png" : 8,
        "PNG-cards-1.3/8_of_hearts.png" : 8,
        "PNG-cards-1.3/8_of_spades.png" : 8,
        "PNG-cards-1.3/9_of_clubs.png" : 9,
        "PNG-cards-1.3/9_of_diamonds.png" : 9,
        "PNG-cards-1.3/9_of_hearts.png" : 9,
        "PNG-cards-1.3/9_of_spades.png" : 9,
        "PNG-cards-1.3/10_of_clubs.png" : 10,
        "PNG-cards-1.3/10_of_diamonds.png" : 10,
        "PNG-cards-1.3/10_of_hearts.png" : 10,
        "PNG-cards-1.3/10_of_spades.png" : 10,
        "PNG-cards-1.3/jack_of_clubs.png" : 11,
        "PNG-cards-1.3/jack_of_diamonds.png" : 11,
        "PNG-cards-1.3/jack_of_hearts.png" : 11,
        "PNG-cards-1.3/jack_of_spades.png" : 11,
        "PNG-cards-1.3/queen_of_clubs.png" : 12,
        "PNG-cards-1.3/queen_of_diamonds.png" : 12,
        "PNG-cards-1.3/queen_of_hearts.png" : 12,
        "PNG-cards-1.3/queen_of_spades.png" : 12,
        "PNG-cards-1.3/king_of_clubs.png" : 13,
        "PNG-cards-1.3/king_of_diamonds.png" : 13,
        "PNG-cards-1.3/king_of_hearts.png" : 13,
        "PNG-cards-1.3/king_of_spades.png" : 13,
        "PNG-cards-1.3/ace_of_clubs.png" : 14,
        "PNG-cards-1.3/ace_of_diamonds.png" : 14,
        "PNG-cards-1.3/ace_of_hearts.png" : 14,
        "PNG-cards-1.3/ace_of_spades.png" : 14,
    }
    card, card_value = random.choice(list(deck.items()))
    return card, card_value

# Stats screen
def load_frame3():
    clear_widgets(frame1) # Clear all the Main menu widgets
    frame3.tkraise() # Raise frame 3 to the top level

    # Header image
    card_img = Image.open("PNG-cards-1.3/ace_of_hearts.png").resize((250, 363))
    card_img_tk = ImageTk.PhotoImage(card_img)
    card_label = tk.Label(frame3, image = card_img_tk)
    card_label.image = card_img_tk
    card_label.pack(pady = 20)
    
    # Display wins
    win = pd.read_sql_query('''
        SELECT COUNT(result) FROM statistics WHERE result LIKE 'win';
        ''', sql_connect)
    
    wins_label = tk.Label(frame3,
                            text = f"Total Wins: {win.iloc[0, 0]}",
                            font = ("TkMenuFont", 20)
    )
    wins_label.pack(pady=10)

    # Display losses
    loss = pd.read_sql_query('''
        SELECT COUNT(result) FROM statistics WHERE result LIKE 'loss';
        ''', sql_connect)
    
    loss_label = tk.Label(frame3,
                            text = f"Total Losses: {loss.iloc[0, 0]}",
                            font = ("TkMenuFont", 20)
    )
    loss_label.pack(pady=10)

    # Display ties
    tie = pd.read_sql_query('''
        SELECT COUNT(result) FROM statistics WHERE result LIKE 'tie';
        ''', sql_connect)
    
    tie_label = tk.Label(frame3,
                            text = f"Total Ties: {tie.iloc[0, 0]}",
                            font = ("TkMenuFont", 20)
    )
    tie_label.pack(pady=10)

    # Counting a tie as 0.5 of a win and 0.5 of a loss and adding to wins/losses
    wins_plus_ties = win.iloc[0, 0] + (tie.iloc[0, 0]/2)
    losses_plus_ties = loss.iloc[0, 0] + (tie.iloc[0, 0]/2)

    # Finding the win percentage by dividing the wins by the wins + losses to get win/loss ratio
    win_percentage = round(float(wins_plus_ties / (wins_plus_ties + losses_plus_ties)), 2)

    # Display win percentage
    wins_label = tk.Label(frame3,
                            text = f"Total Win Percentage: {win_percentage * 100}%",
                            font = ("TkMenuFont", 20)
    )
    wins_label.pack(pady=10)
    
    # Button Back
    back_button = tk.Button(
        frame3,
        text = "Back",
        font = ("TkHeadingFont", 15),
        command = lambda:load_frame1()
        )
    back_button.pack(pady=10)
    
# Establish the frames of the game

# Main menu
frame1 = tk.Frame(main, width=1200, height=800)
frame1.grid(row = 0, column = 0, sticky = "nesw")

# Game screen
frame2 = tk.Frame(main, width=1200, height=800)
frame2.grid(row = 0, column = 0, sticky = "nesw")

# Stats screen
frame3 = tk.Frame(main, width=1200, height=800)
frame3.grid(row = 0, column = 0, sticky = "nesw")

# Load the main menu
load_frame1()


# App run loop
main.mainloop()


#Thank you to 
#https://www.youtube.com/watch?v=5qOnzF7RsNA
#https://www.youtube.com/watch?v=UP_kOuCz88A


# In[ ]:




