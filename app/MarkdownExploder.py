import os
import shutil
import glob
import subprocess
import copy
from jinja2 import Template
import time
import logging    
import logging_loki
from sys import stdout


class DirectoryCrawler(object):

    def __init__(self, content_dir=None, logger=None):
        self.content_dir = content_dir
        self.logger = logger
        self.logger.debug(f'[DC] Directory Crawler Initalized with content_dir of {content_dir}. self.content_dir is {self.content_dir}')

    def create_directory(self, directory_name):
        self.logger.debug(f'[DC] Creating anew directory at {directory_name}')
        os.makedirs(directory_name)

    def destroy_directory(self, directory_name, safe=False):
        if safe:
            shutil.rmtree(directory_name, ignore_errors=False)
        else:
            shutil.rmtree(directory_name, ignore_errors=True)

    def grab_all_markdown_file_paths(self, directory, depth=1):
        patterns = [f'{directory}{ "/*" * level }.md' for level in range(1, depth+1)]
        self.logger.debug(f'[DC] Generated the following patterns based off of {directory = } and {depth = }. {patterns = }')

        # I still think there is a more concise way of doing this, but
        # result = [x for [y] for z]
        #   x   -> for each path in each list
        #   [y] -> generate a list of lists containing all files that match the pattern
        #   z   -> for each list in the generated list
        paths = [path for sublist in [glob.glob(pattern) for pattern in patterns] for path in sublist]
        logging.info(f'[DC] The following markdown paths were discovered: {paths}')

        return paths

    def ingest_data(self, files):

        def _read_all_data_from_file(path):
            with open(path, 'r') as ifile:
                return ifile.read()

        def _generate_name(file_path):

            if self.content_dir != None:
                working_title = file_path.replace(f'{self.content_dir}/', '')
            else:
                working_title = file_path

            return(''.join(working_title.split('.')[:-1]))


        data = {}

        if isinstance(files, str):
            output = _read_all_data_from_file(files)
            data[_generate_name(files)] = output

            self.logger.debug(f'[DC] An excerpt of the data extracted at {files}: {output[:100]}')

        
        if isinstance(files, list):
            for file in files:
                output = _read_all_data_from_file(file)
                data[_generate_name(file)] = output

                self.logger.debug(f'[DC] An excerpt of the data extracted at {file}: {output[:100]}')

        return data

    def get_sequence(self, content_directory=None):

        if content_directory != None:
            sequence = self.ingest_data(f'{content_directory}/sequence.txt')
            sequence = sequence['sequence'].split('\n')
            
            self.logger.debug(f'[DC] Extracted the following sequence from specified content dir {content_directory} : {sequence = }')

            return sequence
        else:
            sequence = self.ingest_data(f'{self.content_dir}/sequence.txt')
            sequence = sequence['sequence'].split('\n')

            self.logger.debug(f'[DC] Extracted the following sequence from the internal content dir {self.content_dir} : {sequence = }')

            return sequence


    def get_markdown_content(self):
        self.logger.debug('[DC] Grabbing all available markdown content')
        paths = self.grab_all_markdown_file_paths(self.content_dir)
        return self.ingest_data(paths)

class MarkdownExploder(object):
    def __init__(self, content_dir, logger):
        self.content_dir = content_dir
        self.logger = logger
        self.db_crawler = None
        self.data = None
        self.sequence = None
        self.staging_dir = None

        self.logger.debug(f'[ME] Markdown Exploder Initalized with content_dir of {content_dir}. self.content_dir is {self.content_dir}')
        self.logger.info(f'[ME] Markdown Exploder initalized: Now grabbing data')

        self.gather_data()

    def __del__(self):
        self.delete_staging()

    def _subprocess_logger(self, process):
        stdout, stderr = process.communicate()
        self.logger.debug(f'[ME] Output from the pandoc command: {stdout = }\n{stderr = } ')


    def gather_data(self):
        self.db_crawler = DirectoryCrawler(self.content_dir, self.logger)
        self.data = self.db_crawler.get_markdown_content()
        self.sequence = self.db_crawler.get_sequence()

        self.logger.debug(f'[ME] Initial data gathering complete. Derived sequence is {self.sequence}. Length of data keys is {len(self.data.keys())}')

    def generate_staging(self, staging_name=None):
        if staging_name is not None:
            self.logger.debug('[ME] Attempting to create staging directory')
            self.staging_dir = staging_name
            self.db_crawler.create_directory(self.staging_dir)
            self.logger.info(f'[ME] Created staging directory with given name of {staging_name}')
        else:
            self.logger.debug('[ME] Attempting to create staging directory')
            self.staging_dir = 'staging'
            self.db_crawler.create_directory(self.staging_dir)
            self.logger.info(f'[ME] Created staging directory with internal name of {self.staging_dir}')

    def compile_markdown_files_into_master_document(self):
        self.logger.debug(f'[ME] Begin merging individual MD files into single file')

        if self.staging_dir == None:
            self.generate_staging()

        master_name = f'{self.staging_dir}/complete_document.md'

        self.logger.debug(f'[ME] Creating master file with name {master_name}')
        with open(master_name, 'w') as outfile:
            for item in self.sequence:
                outfile.write(f'{self.data[item]}\n')

        self.logger.info(f'[ME] Created master file containing all MD sections with the name {master_name}')

        return master_name

    def call_pandoc(self, source_format, target_format, origin, destination, fragment=False):
        # pandoc test1.md -f markdown -t latex -s -o test1.tex
        self.logger.debug(f'[ME] Calling pandoc to convert {origin} from {source_format} to {target_format} and store it at {destination}')
        if not fragment:
            process = subprocess.Popen(['pandoc', origin, '-f', source_format, 
                                        '-t', target_format, '-o', 
                                        destination, '--top-level-division=chapter'],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        
        else:
            process = subprocess.Popen(['pandoc', origin, '-o', destination,],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)

        self._subprocess_logger(process)

        file_created = False
        if os.path.exists(destination):
            file_created = True

        self.logger.info(f'[ME] Successfully executed the command to convert {origin} from {source_format} to {target_format}. File created at {destination} : {file_created}')
    
    def convert_markdown_content_to_latex(self):

        files_to_convert = [(f'{self.content_dir}/{path}.md', f'{self.staging_dir}/{path}.tex') for path in self.data.keys()]

        self.logger.info(f'[ME] Attempting to convert the following files from markdown to latex: {files_to_convert}')

        for file in files_to_convert:
            self.call_pandoc('markdown', 'latex', file[0], file[1])
        
        self.logger.info(f'[ME] Completed the conversion of all files from markdown to latex')

    def generate_homepage(self):
        self.logger.debug(f'[ME] Attempting to create a new homepage')
        # Cleanup Beforehand
        if os.path.exists('home.html'):
            os.remove('home.html')

        # Compile markdown into one and convert to html snippet
        complete_md_content_path = self.compile_markdown_files_into_master_document()
        self.call_pandoc('markdown', 'html', complete_md_content_path, complete_md_content_path.replace('.md', '.html'))

        # Allow 10 seconds for all pandoc commands to complete
        timer = 0
        while (len(glob.glob("staging/*.html")) < 1) and (timer < 10):
            timer += 1
            time.sleep(1)

        if len(glob.glob("staging/*.html")) == 0:
            self.logger.warning('Pandoc call seems to have failed. complete_document.html never generated')

        # Grab template content
        sidebar_items = [' '.join(item.split('_')).upper() for item in self.sequence]
        home_content = ''
        with open(complete_md_content_path.replace('.md', '.html'), "r") as ifile:
            home_content = ifile.read()

        self.logger.debug("[ME] Grabbing template from /templates")
        j_template = ''
        with open('templates/home_template.html', 'r') as ifile:
            j_template = ifile.read()

        self.logger.debug('[ME] Initalizing Template')
        home = Template(j_template)

        self.logger.debug(f'[ME] Passing {sidebar_items = } and content = {home_content[:100]} to Jinja for creation')
        home.stream(section_list=sidebar_items, content=home_content).dump('home.html')

        # logging test
        if os.path.exists('home.html'):
            self.logger.info('[ME] New homepage successfully created')
        else:
            self.logger.warning('[ME] No file detected at home.html. Creation seems to have failed')

    def generate_latex_document(self):
        self.logger.debug(f'[ME] Attempting to create a new LaTeX document')
        # cleanup beforehand
        if os.path.exists('assets/SethAngellCapstone.pdf'):
            os.remove('assets/SethAngellCapstone.pdf')

        # Generate LaTeX Files
        self.convert_markdown_content_to_latex()
        time.sleep(10)

        # Allow 10 seconds for all pandoc commands to complete
        timer = 0
        while (len(glob.glob("staging/*.tex")) < 6) and (timer < 10):
            timer += 1
            time.sleep(1)

        if len(glob.glob("staging/*.tex")) == 0:
            self.logger.warning('Pandoc call seems to have failed. No LaTeX documents were ever generated')

        # Create PDF
        # pdflatex -output-directory=DIR -jobname=STRING FILE
        process = subprocess.Popen(['pdflatex', '-output-directory=assets', 
                                    '-jobname=SethAngellCapstone', 'templates/capstoneSeth.tex'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)

        self._subprocess_logger(process)


        for file in [f'assets/SethAngellCapstone{ending}' for ending in ['.aux', '.out', '.toc', '.log']]:
            if os.path.exists(file):
                os.remove(file)
                self.logger.debug(f'[ME] Deleted {file}')

    def delete_staging(self):
        self.db_crawler.destroy_directory(self.staging_dir, False)

def generate_logging_handler():
    print(f'{"="*120}')
    loki_user = os.getenv('loki_user')
    loki_pass = os.getenv('loki_pass')
    print(f'{loki_user = }, {loki_pass = }')
    print(f'{"="*120}')
    handler = logging_loki.LokiHandler(
    url="http://http://150.136.244.134:3100/loki/api/v1/push", 
    tags={"application": "MarkdownExploder"},
    auth=(loki_user, loki_pass),
    version="1",
    )

    return handler

if __name__ == "__main__":

    logger = logging.getLogger('MarkdownExploder')
    logger.addHandler(generate_logging_handler())
    if os.getenv('DEBUG'):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    MD = MarkdownExploder('content', logger)
    MD.generate_homepage()
    MD.generate_latex_document()


