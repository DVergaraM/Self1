# Second Brain - Source Code


This folder contains the source code for the Second Brain application. Second Brain is a personal knowledge management system that allows users to store and organize information in a centralized location.


## File Structure
  
The `src/` folder contains the following files and subfolders:


- `__main__.py`: The main file of the application that initializes the GUI and starts the event loop.

- `logic/`: A subfolder containing the core logic of the application, including modules for managing notifications, running threads, and interacting with the database.

- `utils/`: A subfolder containing utility modules for setting configuration options and making connections between GUI elements and methods.

- `ui/`: A subfolder containing UI files for the various GUI menus and dialogs.

The `assets/` folder contains the following files

  
## Dependencies

The Second Brain application has the following dependencies:

- Python 3.10 or higher

- [PyQt5](https://pypi.org/project/PyQt5/)
    - For the GUIs and threads

- [PyStray](https://pypi.org/project/pystray/)
    - For the System Tray Icon

- [Winotify](https://pypi.org/project/winotify/)
    - For the Notification System

- [Schedule](https://pypi.org/project/schedule/)
    - For running methods at certain hours

- [Pillow](https://pypi.org/project/Pillow/)
    - For loading images


## Running the Application


To run the Second Brain application, run the `src/` folder using Python:  

```
python setup.py && python src
```
  
This will start the application and display the login dialog. Once you have logged in, you will be taken to the main GUI of the application.

  

## Contributing

If you would like to contribute to the Second Brain application, please fork this repository and submit a pull request with your changes. We welcome contributions of all kinds, including bug fixes, new features, and documentation improvements.

  

## License

The Second Brain application is licensed under the MIT License. See the `LICENSE` file for more information.