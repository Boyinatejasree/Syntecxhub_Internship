# Syntecxhub_Todo_List_Manager

A menu-driven command-line To-Do List Manager built in Python for the Syntecxhub Python Programming internship (Week 1, Project 3).

## Features
- Add, view, delete, and mark tasks as done
- Tasks are saved to `tasks.json`, so they survive restarts
- Optional due dates (YYYY-MM-DD) with overdue flagging
- Optional tags and filtering by tag
- Error handling for invalid input and file problems
- Logic functions kept separate from input/output functions

## Requirements
- Python 3.8 or newer (no external libraries needed)

## How to run
```
python todo_manager.py
```
(Use `python3` on Mac/Linux.)

## Menu
1. Add task
2. View all tasks
3. Mark task done
4. Delete task
5. Filter by tag
6. Exit

## Project structure
```
Syntecxhub_Todo_List_Manager/
├── todo_manager.py   # main program
├── README.md
└── .gitignore
```
