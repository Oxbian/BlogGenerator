# Blog Generator

This repo contains a python script that can create a blog from a list of markdown files. You just need markdown files, a page template, an index page template, an atom feed template and an atom post template.  
If you need some example check my [blog source code](https://git.arka.rocks/Oxbian/ArkaBlog).  

## How to setup

First you will need some compatible written markdown files, the supported markdown is listed below.  
After that, you will need to setup the .env file with your configuration and create template for the page, index, Atom Feed & Atom post.  
  
Now that is done, you will need to install the dependencies.  
There is two solutions:

### First solution virtual env

You can create a [virtual python environment](https://docs.python.org/3/library/venv.html) 
```bash
python -m venv .venv
``` 
and install the `requirements.txt`  

```bash
pip intall -r requirements.txt
```

### Second solution install on your global python

Don't create / use virtual env, just install the requirements on your global python.

```bash
pip intall -r requirements.txt
```

## How to use it 

Now that everything is configured, you can just run `python3 generator.py` and the page will be generated.  
**Be careful if there is no metadata in your markdown file the page will not be added into the index page.**  

## Supported markdown

Here is listed the supported markdown for this blog generator :  

### Line type

- `#` for title, every line with this will be considered as the title, so only use one.
- `##`, `###`, `####` for h2, h3, h4.
- ` ``` ` for bloc code
- `>` for quote
- `-` for listing (ul > li)

A line which start without this will be considered as a paragraph.  

### Line content

- `*` for emphasis text
- `**` for strong text
- `![image text](image link)` for image
- `[link text](link)` for link

### Metadata

For creating metadata you need to use `---` before and after the metadata.
Example: 
```
---
date: 31-12-1999
description: new year
tags: new year, happy, test
---
```

- `date:` for date
- `description:` for description
- `tags:` for tags

## Dependencies

This project only has `python-dotenv` as dependencies for loading environment variable into python.  

## Trouble & help

If you have any troube you can contact me by email, matrix, or open an issue. If you are a beginner prefer using email, thanks.

- Email: oxbian.noch@simplelogin.com
- Matrix: @oxbian:matrix.org

## License

This project is under the GPLV3 license. You can use, modify, as long as the copy is opensource under the GPLV3 too.

## Credits

This project was inspired by the [blog generator](https://git.sr.ht/~lioploum/ploum.net) made by [Ploum](https://ploum.net), thanks to him for his work.

