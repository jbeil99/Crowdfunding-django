# Django Project Setup 

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/jbeil99/django-project.git
    cd django-project
    ```

2.  **Create a Virtual Environment (Recommended):**

    While `uv` manages dependencies, a virtual environment is still useful for isolating your project. This step is optional but strongly recommended.

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate      # On Windows
    ```

3.  **Install Dependencies using uv:**

    Use `uv` to install the project dependencies based on the `pyproject.toml` and `uv.lock` file.

    ```bash
    uv pip install .
    ```
    If you do not have uv.lock, and need to create it from pyproject.toml, run this command instead.
    ```bash
    uv pip sync
    ```

4.  **Migrate the Database:**

    If your Django project uses a database, apply the migrations:

    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (If Necessary):**

    If you need to access the Django admin panel, create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Development Server:**

    Start the Django development server:

    ```bash
    python manage.py runserver
    ```

    This will start the server, and you can access your Django application in your web browser at `http://127.0.0.1:8000/`.
    
## Adding New Libraries and Dependencies

When you need to add a new library or dependency to your project, follow these steps:

1.  **Use `uv pip add`:**

    Use the `uv pip add` command to add the new library to your `pyproject.toml` file. For example, to add the `requests` library:

    ```bash
    uv pip add requests
    ```

    You can specify version constraints as needed:

    ```bash
    uv pip add django>=4.2
    ```

2.  **Synchronize the Dependencies:**

    After adding the library, synchronize the dependencies to update the `uv.lock` file and install the new library:

    ```bash
    uv pip sync
    ```

    This command will ensure that all dependencies are installed according to the specifications in your `pyproject.toml` and `uv.lock` files.

3.  **Verify Installation:**

    You can verify that the library has been installed by running:

    ```bash
    uv pip list
    ```

    This will display a list of installed packages.
## Important Notes

* **`uv.lock` File:** The `uv.lock` file ensures consistent dependency versions across different environments. Do not modify this file manually. If you are adding a new dependency, use `uv pip add <package_name>` and then `uv pip sync`.
* **`pyproject.toml`:** The `pyproject.toml` file declares the project's dependencies and build system requirements. Modify this file as needed to update your project's dependencies.
* **`.gitignore`:** Ensure your `.gitignore` file includes `venv/` (if using a virtual environment) and any other sensitive files or directories.
* **Database Configuration:** Check your `settings.py` file to ensure the database settings are correct for your environment.
* **Static Files:** If your project uses static files, you may need to run `python manage.py collectstatic` to collect them into a single directory for deployment.
* **Environment Variables:** For sensitive data like database passwords or API keys, use environment variables instead of hardcoding them in your `settings.py` file.