import os
import shutil
import glob
import subprocess
from jinja2 import Template
import time

class DirectoryCrawler(object):

    def __init__(self, content_dir=None):
        self.content_dir = content_dir

    def create_directory(self, directory_name):
        os.makedirs(directory_name)

    def destroy_directory(self, directory_name, safe=False):
        if safe:
            shutil.rmtree(directory_name, ignore_errors=False)
        else:
            shutil.rmtree(directory_name, ignore_errors=True)

    def grab_all_markdown_file_paths(self, directory, depth=1):
        patterns = [f'{directory}{ "/*" * level }.md' for level in range(1, depth+1)]

        # I still think there is a more concise way of doing this, but
        # result = [x for [y] for z]
        #   x   -> for each path in each list
        #   [y] -> generate a list of lists containing all files that match the pattern
        #   z   -> for each list in the generated list
        paths = [path for sublist in [glob.glob(pattern) for pattern in patterns] for path in sublist]

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

        
        if isinstance(files, list):
            for file in files:

                output = _read_all_data_from_file(file)

                data[_generate_name(file)] = output

        return data

    def get_sequence(self, content_directory=None):

        if content_directory != None:
            sequence = self.ingest_data(f'{content_directory}/sequence.txt')
    
            sequence = sequence['sequence'].split('\n')

            return sequence
        else:
            sequence = self.ingest_data(f'{self.content_dir}/sequence.txt')
    
            sequence = sequence['sequence'].split('\n')

            return sequence


    def get_markdown_content(self):
        paths = self.grab_all_markdown_file_paths(self.content_dir)
        return self.ingest_data(paths)

class MarkdownExploder(object):
    def __init__(self, content_dir):
        self.content_dir = content_dir
        self.db_crawler = None
        self.data = None
        self.sequence = None
        self.staging_dir = None

        self.gather_data()

    def __del__(self):
        print('cleaning up')
        self.delete_staging()

    def gather_data(self):
        self.db_crawler = DirectoryCrawler(self.content_dir)
        self.data = self.db_crawler.get_markdown_content()
        self.sequence = self.db_crawler.get_sequence()

    def generate_staging(self, staging_name=None):
        if staging_name is not None:
            self.staging_dir = staging_name
            self.db_crawler.create_directory(self.staging_dir)
        else:
            self.staging_dir = 'staging'
            self.db_crawler.create_directory(self.staging_dir)

    def compile_markdown_files_into_master_document(self):
        if self.staging_dir == None:
            self.generate_staging()

        master_name = f'{self.staging_dir}/complete_document.md'

        with open(master_name, 'w') as outfile:
            for item in self.sequence:
                outfile.write(f'{self.data[item]}\n')

        return master_name

    def call_pandoc(self, source_format, target_format, origin, destination, fragment=False):
        # pandoc test1.md -f markdown -t latex -s -o test1.tex
        if not fragment:
            process = subprocess.Popen(['pandoc', origin, '-f', source_format, 
                                        '-t', target_format, '-o', 
                                        destination,],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(['pandoc', origin, '-o', destination,],
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
    
    def convert_markdown_content_to_latex(self):

        files_to_convert = [(f'{self.content_dir}/{path}.md', f'{self.staging_dir}/{path}.tex') for path in self.data.keys()]

        for file in files_to_convert:
            self.call_pandoc('markdown', 'latex', file[0], file[1])

    def generate_homepage(self):
        # Cleanup Beforehand
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
            raise RuntimeError('Pandoc call seems to have failed. complete_document.html never generated')

        # Grab template content
        sidebar_items = [' '.join(item.split('_')).upper() for item in self.sequence]
        home_content = ''
        with open(complete_md_content_path.replace('.md', '.html'), "r") as ifile:
            home_content = ifile.read()

        j_template = ''
        with open('templates/home.html', 'r') as ifile:
            j_template = ifile.read()

        home = Template(j_template)

        home.stream(section_list=sidebar_items, content=home_content).dump('home.html')

    def delete_staging(self):
        self.db_crawler.destroy_directory(self.staging_dir, False)




    


                



test = DirectoryCrawler('content')

test.grab_all_markdown_file_paths('content', 5)

test.get_sequence('content')

MD = MarkdownExploder('content')
MD.compile_markdown_files_into_master_document()
MD.convert_markdown_content_to_latex()
MD.generate_homepage()
MD.delete_staging()


