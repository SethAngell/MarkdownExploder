# Markdown Exploder
### A Markdown → LaTeX + HTML Workflow

[![deploy](https://github.com/SethAngell/MarkdownExploder/actions/workflows/deploy.yml/badge.svg)](https://github.com/UNCWMixedReality/VASCTeacherPortal/actions/workflows/deploy.yml)


## Use Case

I love markdown for it's simplicity and lack of distractions. Over the years, it has become a stronghold for me to fall back to when I feel like I'm overwhelmed or distracted. When it came time to draft out the first version of my capstone thesis, I retreated all the way into a `vim introduction.md` as a way to shut out everything except for my work. Except there was 1 problem, I needed to convert 8 different markdown files into a single LaTeX report. Because automating annoying tasks in 99% of the reason I got into computer science, enter...__Markdown Exploder.__

Markdown Exploder is a simple workflow enabled by _python, pandoc, and LaTex_. Sections are written in markdown, organized with a single `sequence.txt` file, and then compiled into a static html page and LaTeX report.

You can see a working version (with a very sparse paper) at [https://capstone.sethangell.com](capstone.sethangell.com)!

## Ideal Workflow

1. Create a LaTeX document which provides a basic structure for my document and expects a collection of files using the \input directive.
2. Create an HTML homepage template which expects a block of HTML content and some navigation tags, representing my paper.
3. Write a bunch of markdown in a directory organized as a collection of high level sections of my Capstone Proposal (Introduction, Methodology, etc)
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
- [x] Create Jinja Base Template
- [x] Create LaTeX Base Template
- [x] Find and include all commands to install LaTeX into Build container
- [x] Create python functionality for creating and destroying new directories
- [x] Create python functionality for ingesting all data from the content directory
- [x] Create python functionality for calling pandoc commands
- [x] Create python functionality for concatenating markdown documents into single file
- [x] Create python functionality for converting all markdown content into LaTeX fragments
- [x] Create python functionality for compiling LaTeX documents to pdfs
- [x] Create python functionality for compiling final html
- [x] BONUS! Dockerfile.Prod which also runs letsencrypt and stores it on the host 
- [x] BONUS! Github Actions CI to automatically deploy new changes on every push

## MarkdownExploder Writing Workflow
![A state diagram of the intended writing workflow utilizing Markdown Exploder](/app/assets/MarkdownExploderWorkflow.png)

## Preprocessing Workflow
![A basic state diagram](/app/assets/PythonPreprocessingPipeline.png)



