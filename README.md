# Film Explorer Application

## Overview

Film Explorer is a Python-based application that allows users to browse, search, and filter films based on various criteria such as title, genre, release date, runtime, rating, language, and type. Users can also manage their personal lists of films to watch and films they have watched.

## Features

- **User Management**: Create, login, and manage user accounts.
- **Film Search**: Search films by title or genre.
- **Film Filtering**: Filter films by release date, runtime, rating, language, and type.
- **User Lists**: Manage personal lists of films to watch and films already watched.
- **Data Scraping**: Automatically scrape film data from IMDb and Wikipedia.
- **GUI**: User-friendly graphical interface built with Tkinter.

## Usage

### User Login

- **New User**: Enter a username and password, then click "Login as new user".
- **Existing User**: Enter your username and password, then click "Login".

### Main Interface

- **Search**: Enter a film title or genre to search for films.
- **Filters**: Apply various filters such as release date, runtime, rating, language, and type.
- **Context Menu**: Right-click on a film to add it to your "To Watch" or "Watched" lists.
- **User Menu**: Access the "My User" menu to log out or delete your account.

## File Structure

- `GUI.py`: Contains the main application interface.
- `user_handler.py`: Manages user accounts and their film lists.
- `data_scraper.py`: Scrapes and processes film data from external sources.
- `film_list.py`: Handles film data and provides search and filter functionality.

## Dependencies

- `tkinter`: Standard Python interface to the Tk GUI toolkit.
- `ttkthemes`: Themed widgets for Tkinter.
- `pandas`: Data manipulation and analysis library.
- `requests`: Library for making HTTP requests.
- `beautifulsoup4`: Library for web scraping.
- `gzip`: Library for handling gzip files.
- `shutil`: Library for high-level file operations.
