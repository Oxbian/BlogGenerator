import os
import dotenv
from markdown_parser import *
from datetime import datetime

def md2html(filename, env_vars):
    """
    Create the html webpage from template and markdown content
    filename: file to transform into HTML
    env_vars: dictionnary of env variables
    return: a dictionnary containing title, metadata, local path, content for HTML
    """
    # Getting parsed content of markdown file & page template
    data = parsemd(filename, env_vars)
    template = open(env_vars['template_page'], 'r').read()

    # Generating the HTML page
    output = open(env_vars['pages_path'] + '/' + filename.split('.')[0] + '.html', 'w')
    output.write(template.replace("$CONTENT", data['content']).replace("$TITLE", data['title']).
     replace("$DATE", data['date']).replace("$DESC", data['description']))
    output.close()

    return data


def generatePageXML(data, env_vars):
    """
    Generate a RSS / Atom post for the page
    data: dictionnary generated by the markdown parser
    env_vars: dictionnary of env variables
    return: RSS / Atom post
    """
    template = open(env_vars['template_atom_post'], 'r').read()
    date = datetime.strptime(data['date'],"%d-%m-%Y").isoformat() + "Z"
    return template.replace("$TITLE", data['title']).replace("$DATE", data['date']).replace("$CONTENT", 
     data['content']).replace("$URL", env_vars['website_url'] + data['filepath'])
    

def generateAtomFeed(posts, env_vars):
    """
    Generate a RSS / Atom feed
    posts: list of data get from markdown pages
    env_vars: dictionnary of env variables
    """
    # Generate RSS / Atom post
    atom_content = []
    for post in posts:
        generatePageXML(post, env_vars)

    # Generate RSS / atom feed
    template = open(env_vars['template_atom_feed'], 'r').read()
    output = open(env_vars['parent_path'] + '/atom.xml', 'w')
    output.write(template.replace("$CONTENT", atom_content))
    output.close()


def generateIndex(data, env_vars):
    """
    Generate the main page
    data: list of data get from markdown pages
    env_vars: dictionnary of env variables
    """
    # Create the index content
    index_content = "<ul>"
    for page in data:
        index_content += '<li><a href="' + page['filepath'] + '">' + page['title'] + '</a><p>'
        + page['date'] + '</p></li>\n'
    index_content += "</ul>"

    # Generate main page
    template = open(env_vars['template_index'], 'r').read()
    output = open(env_vars['parent_path'] + '/index.html', 'w')
    output.write(template.replace("$CONTENT", index_content))
    output.close()


if __name__=="__main__":
    # Load .env file into python environment
    dotenv.load_dotenv()

    # Color for print
    color = { 'red': '\033[1;31m', 'green' : '\033[1;32m', 'end' : '\033[0m'}

    # Checking if all environment variable are present  & setup
    env = ['PARENT_PATH', 'PAGES_PATH', 'MARKDOWN_PATH', 'TEMPLATE_PAGE', 'TEMPLATE_ATOM_POST', 
           'TEMPLATE_ATOM_FEED', 'WEBSITE_URL', 'TEMPLATE_INDEX']
    for variable in env:
        if variable not in os.environ:
            print(f"{color['red']}{variable} isn't present in the .env file, please fix this {color['end']}")
            quit()

        if (os.environ.get(variable) or '') == '':
            print(f"{color['red']}{variable} isn't setup in the .env file, please fix this {color['end']}")
            quit()

    # Getting env variable
    env_vars = { 'parent_path' : os.environ.get('PARENT_PATH'), 'pages_path' : os.environ.get('PAGES_PATH')
    , 'markdown_path' : os.environ.get('MARKDOWN_PATH'), 'template_page' : os.environ.get('TEMPLATE_PAGE')
    , 'template_atom_post' : os.environ.get('TEMPLATE_PAGE'), 'template_atom_feed' : os.environ.get('TEMPLATE_ATOM_FEED')
    , 'website_url' : os.environ.get('WEBSITE_URL'), 'template_index' : os.environ.get('TEMPLATE_INDEX') }

    # Checking if generate folder exist to remove previouly generated content, if not create it
    if os.path.exists(env_vars['pages_path']):
        for file in os.listdir(env_vars['pages_path']):
            os.remove(env_vars['pages_path'] + '/' + file)
        os.remove(env_vars['parent_path'] + '/atom.xml')
        os.remove(env_vars['parent_path'] + '/index.html')
    else:
        os.mkdir(env_vars['pages_path'])

    # Generate all markdown file
    for file in os.listdir(env_vars['markdown_path']):

        # Generating HTML page
        print(f"{color['green']}Generating file: {file} {color['end']}")
        data = [] # A list for data generated by md2html
        data.append(md2html(file, env_vars))

        sorted_data = sorted(data, key=lambda x:datetime.strptime(x['date'], '%d/%m/%Y'))

        # Generating atom feed
        print(f"{color['green']}Generating RSS / Atom feed {color['end']}")
        generateAtomFeed(data, env_vars)
        
        # Generating index 
        print(f"{color['green']}Generating main page {color['end']}")
        generateIndex(data, env_vars)