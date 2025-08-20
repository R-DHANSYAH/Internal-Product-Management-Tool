# Internal Product Management Tool


A simple **Flask-based web application** to manage **categories, products, attributes, and attribute values**.  
The tool allows you to create, edit, delete, and assign attribute values to products. Designed for internal use, it features a clean UI and pagination support.

---

## Features

- **Dashboard / Home** page with navigation links to all modules  
- **Category Management**: Add, Edit, Delete categories  
- **Attribute Management**: Add, Edit, Delete attributes, linked to categories  
- **Product Management**: Add, Edit, Delete products, linked to categories  
- **Assign Attribute Values**: Assign, Update, Delete attribute values for products  
- **Persistent Navbar** for easy navigation across all pages  
- **Pagination** for categories, attributes, products, and values  
- Flash messages for user-friendly feedback  

---

## Tech Stack

- **Backend**: Python 3.13, Flask  
- **Database**: SQLite (via SQLAlchemy ORM)  
- **Frontend**: HTML, CSS  
- **Dependencies**: Listed in `requirements.txt`
  
  ---
  ## Diagrams
  ![ERD](Diagrams/ERD.png)
  ![Class Diagram](Diagrams/Classdiagram.png)
 

