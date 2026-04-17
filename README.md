# TechStore (Laptop Store)

A robust Django-based e-commerce backend tailored specifically for selling laptops and computer hardware. It features a heavily customized admin interface and a specialized product database schema.

## 🚀 Features

* **Detailed Product Inventory**: Manage laptop specifications precisely with dedicated fields for CPU, RAM, GPU, and Storage.
* **Order Management System**: Track customer orders through multiple lifecycle stages including Pending, In Progress, Completed, and Cancelled.
* **Dynamic Store Configuration**: Easily update store branding (logo), WhatsApp contact, and Facebook links directly from the admin panel. 
* **Performance Caching**: Store settings are automatically cached to ensure high performance and fast page loads.
* **Premium Admin Dashboard**: Features a customized "Black & Gold Premium" UI via Django Jazzmin, complete with Arabic localization and tailored navigation icons.
* **API Ready**: Integrates Django REST Framework for seamless frontend or mobile application connections.

## 🛠️ Tech Stack

* **Backend**: Python 3, Django 5.2.12.
* **Database**: SQLite3 (Default).
* **Admin Interface**: Django Jazzmin.

## 📦 Prerequisites

Ensure you have the following installed before setting up the project:
* Python 3.x
* pip (Python package installer)

The project relies on several key packages that should be in your `requirements.txt`:
* `Django`
* `django-jazzmin`
* `djangorestframework`
* `django-phonenumber-field`
* `python-dotenv`
* `Pillow` (Required for `ImageField` image uploads)

## ⚙️ Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/O-A-Suliman/Laptop_Store-.git
   cd Laptop_Store
