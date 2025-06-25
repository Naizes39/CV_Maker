# CV_Maker

CV_Maker is a web application that allows users to generate professional-looking CVs in PDF format. It features a user-friendly web interface for data entry and a powerful LaTeX-based backend for high-quality document generation.

## Features

- **Web-based Interface**: Easily create and edit your CV content through a web form.
- **Multiple Sections**: Supports various CV sections like Summary, Experience, Education, Skills, Projects, and more.
- **PDF Generation**: Creates clean, well-formatted PDF documents using a LaTeX template.
- **Customization**: The architecture supports tailoring CVs for specific job applications using a Builder pattern.
- **REST API**: A Flask-based backend provides an API for CV generation.

## Project Structure

The project is divided into a `frontend` and a `backend`.

- **Backend**: A Python Flask application located in the `backend/` directory.
  - It uses a `SectionFactory` to construct different parts of the CV.
  - A `CVBuilder` allows for programmatic modification of a base CV.
  - A `LaTeXStrategy` handles the final PDF rendering.
- **Frontend**: A simple HTML/CSS/JS interface in the `frontend/` directory for users to input their CV data.

To run the backend, navigate to `backend/` and run `python app.py`. The frontend can be opened by loading `frontend/pages/home.html` in your browser.