# Markdown → LaTeX + HTML Workflow

## Use Case

I’m a markdown lover and ADHD ridden fool who will spend too long playing with systems and not enough time actually creating content. However I have people who expect my content to be in a certain form. For this reason, I’d like to create a workflow which allows me to write in basic markdown format from a text editor or terminal interface, and then with a single command convert this into all the desired formats.

## Ideal Workflow

1. Create a LaTeX document which provides a basic structure for my document and expects a collection of files using the \input directive
2. Create an HTML file which basically contains everything for the webpage and expects only a block of HTML which represents my paper itself
3. Write a bunch of markdown directly in a directory, into a collection of files representing high level sections of my Capstone Proposal (Introduction, Methodology, etc)
4. Run a command which…
   1. converts the individual markdown files into their equivalent LaTeX form
   2. compiles all of the markdown file into a single file
   3. generates a LaTeX PDF based off of the structure mentioned before
   4. generates an html block from the single markdown file and places it inside of the larger html file
   5. generates a docker image which hosts all of this and makes it available with a nginx reverse proxy

## Requirements

- Should require minimal fussiness after set up
- Should play nicely living in a git repository
- Should source images from a single folder. I create an assets folder, I place images into the assets folder, everyone is happy and knows to pull from the assets folder
- We should generate a compiled LaTeX PDF
- We should generate a valid HTML webpage

## Tools For This Project

- Pandoc
- Docker
- LaTeX
- Nginx
- Python
- Jinja

## Running ToDo

- [x] Create directory and Git repository
- [x] Create README
- [ ] Create Jinja Base Template
- [ ] Create LaTeX Base Template

## Preprocessing Workflow
![A basic state diagram](/assets/PythonPreprocessingPipeline.png)

