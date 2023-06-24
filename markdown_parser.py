import html

def parseline(line):
    """
    Parse a line of texte to replace HTML specialchars, link, and strong / emphased of markdown for HTML
    return: the line ready for HTML
    """
    # Change &, <, > for HTML support
    html.escape(line)

    # Checking if there is strong or emphasized
    while '*' in line:
        line = line.replace('*', '<em>', 1)
        line = line.replace('*', '</em>', 1)
    while '**' in line:
        line = line.replace('**', '<strong>', 1)
        line = line.replace('**', '</strong>', 1)

    # Checking if there is image
    while '![' in line and ']' in line:
        title = line.split(']')[0].split('[')[1]
        link = line.split(']')[1].split('(')[1].split(')')[0]
        line = line.replace('![' + title + '](' + link + ')', '<img src="' + link + '" alt="' + title + '"/>')
            
    # Checkinf if there is link
    while '[' in line and ']' in line:
        title = line.split(']')[0].split('[')[1]
        link = line.split(']')[1].split('(')[1].split(')')[0]
        line = line.replace('[' + title + '](' + link + ')', '<a href="' + link + '">' + title + '</a>')

    return line


def parsemd(env_vars, filepath):
    """
    Parse the markdown file and return the content to put into the template page
    env_vars: dictionnary of environment variable
    filepath: Filepath of the markdown file
    return: a dictionnary containing title, metadata, local path, content for HTML
    """
    content = {'content': '', 'title': '', 'date': '', 'description': '', 'filepath': env_vars['pages_path'].replace(env_vars['parent_path'] + '/', '') 
     + '/' + filepath.split('.')[0] + '.html'}
    
    inmeta, inquote, inpre, inul = False, False, False
   
    # Reading the content of the file and transform into html 
    for line in open(env_vars['markdown_path'] + '/' + filepath, "r"):
        line = line.strip()

        # Open the metadata
        if line.startswith('---'):
            if inmeta:
                inmeta = False
            else:
                inmeta = True

        # Getting the date metadata
        if inmeta and line.startswith('date:'):
            content['date'] = line.split(':')[1].strip()
        
        # Getting the description metadata
        if line.startswith('description:'):
            content['description'] = line.split(':')[1].strip()
        
        # Close quote if not quoting
        if inquote and not line.startswith(">"):
            content['content'] += "</blockquote>\n"
            inquote = False
        
        # Close list if not listing
        if inul and not line.startswith("-"):
            content['content'] += "</li>\n</ul>\n"
            inul = False
        
        # Checking if it's a code block
        if line.startswith("```"):
            if inpre:
                content['content'] += "</code></pre>\n"

            content['content'] += "<pre><code>" + line.lstrip("```")
            inpre = True

        # Checking if it's a quote
        elif line.startswith(">"):
            if inquote:
                content['content'] += parseline(line.lstrip("> "))
            else: 
                content['content'] += "<blockquote>" + parseline(line.lstrip("> "))
                inquote = True

        # Checking if it's a list
        elif line.startswith("-"):
            if inul:
                content['content'] += "</li>\n"
                content['content'] += "<li>" + parseline(line.lstrip("- "))
            else:
                content['content'] += "<ul><li>" + parseline(line.lstrip("- "))
                inul = True
        
        # Checking if it's a title
        elif line.startswith("###"):
            content['content'] += "<h3>" + parseline(line.lstrip("# ")) + "</h3>\n"
        elif line.startswith("##"):
            content['content'] += "<h2>" + parseline(line.lstrip("# ")) + "</h2>\n"
        elif line.startswith("#"):
            content['title'] += parseline(line.lstrip("# "))

        # else it's a paragraph
        elif line != " " and line != "":
            content['content'] += "<p>" + parseline(line) + "</p>\n"

    # Checking all balise are closed
    if inquote:
        content['content'] += "</blockquote>\n"
        inquote = False

    if inul:
        content['content'] += "</li></ul>\n"
        inul = False
        
    if inpre:
        content['content'] += "</code></pre>\n"
        inpre = False

    return content

