# Spider

Project allows web scraping. Project can download some web page and iterate over found urls 
recursively. Downloaded pages are converted to simply text files. 

For now project can download and extract text from following formats:

- `html` (obviously html is covered by this project :blush:)
- `pdf` (if there is no restriction from text extraction from it)
- `zip` (project extracts files from it and try to extract text from unzipped files)

## Requirements

Before start, install required dependencies.

```console
python -m pip install -r requirements.txt
```

## Tests

You can run tests by following command:

```console
nose2 -c nose2.cfg
``` 

## Examples

For run, first you can edit `spider/app.py` and define what you want to download.

For example lets assume we want to download texts from `www.somewebpage.com`:

```python

if __name__ == "__main__":

    App(
        url="https://www.somewebpage.com",
        exclude_prefixes=["https://www.youtube.com",
                          "https://www.linkedin.com",
                          ...
                          "http://help.opera.com"],
        exclude_contains=["login", "javascript:void(0)", "#", "phone:", "mailto", "verisign"],
        include_contains=["somewebpage.com"],
        max_depth=1000
    ).main()

```

Where:

- `url` - start url for our application
- `exclude_prefixes` - list of unwanted prefixes (sometimes `url` can contain urls to remote web sites and downloading it is too broad for us). By this attribute we define excluded prefixes
- `exclude_contains` - list of unwanted strings in urls. For example we don't want to download `login.domain.com`, because we have not credentials
- `include_contains` - list of wanted strings in downloaded urls. **You have to define at least ONE value here** or you download nothing.
- `max_depth` - maximum number of recurrence calls 

There are also more parameters:

- `proxy_host` - you can define proxy if needed
- `proxy_user` - if proxy requires user, you can define it here
- `proxy_password` - password for proxy user
- `output_dir` - output dir for downloaded files
- `output_zip` - output file name (zipped texts downloaded from `url`)

## How to run it

To run `app.py` you have to do three simple steps:

1. For linux:

```bash
cd [SPIDER_DIR]
PYTHONPATH=$(pwd)
python spider/app.py

```

2. For Windows:

```bash
cd [SPIDER_DIR]
set PYTHONPATH=%cd%
python spider/app.py
```

Where: 
- `SPIDER_DIR` - root dir for spider project

Important is defining spider project as a module (we add it to `PYTHONPATH` variable).

If everything is OK, spider starts downloading `html`, `pdf` and `zip` files from the internet. 

## How it works

Application does following tasks:

1. Download specified web page 
2. Save it into *html* directory
3. Extract text from html file and save it into *txt* directories
4. Retrieve url links from base page
5. Start next iteration for url links found at point 4


###### HTML 

For example lets assume we downloaded page `https://www.fake.com?param=value`. Structure is as follows:

```console
├── output_dir
│   ├── html
│   │   ├──     https_www_fake_com_param_value.html
│   │   ├──     ...
│
│   ├── txt
│   │   ├──     https_www_fake_com_param_value.txt
│   │   ├──     ...
│   
├── ...
```

Assume, we downloaded following *html* file:

```html
<html>
    <head></head>
    <body>
        <h1>Article Title</h1>
        <div>Some content here</div>
        <div>Another text here</div>
    </body>
</html>
```

In `output_dir/html` we have copy of above html.

In `output_dir/txt` we have all text extracted from html as multiple lines (every html tag as one line):

```text
Article Title
Some content here 
Another text here
```

###### PDF

Now lets assume we found some *pdf* file and also want to download it. 
Url is `https://www.fake.com/file.pdf`. Output directory is as follows:

```console
├── output_dir
│   ├── pdf
│   │   ├──     https_www_fake_com_file.pdf
│   │   ├──     ...
│
│   ├── pdf2txt
│   │   ├──     https_www_fake_com_file.txt
│   │   ├──     ...
│   
├── ...
```

In `output_dir/pdf` we have original pdf file.
In `output_dir/pdf2text` we have text extracted from pdf.

**IMPORTANT:** For text extraction we use [pdfminer3](https://pypi.org/project/pdfminer3/) which is great but very slow.
So by using this app you have to decide whether you want to download pdf files or not.

###### ZIP

Sometimes url links are zipped files. Lets assume we found some *zip* file and also want to download it.
Url is `https://www.fake.com/file.zip`. Output directory is as follows:

```console
├── output_dir
│   ├── zip
│   │   ├──     https_www_fake_com_file.zip
│   │   ├──     ...
│
│   ├── unzipped
│   │   ├──     file_from_zip1.txt
│   │   ├──     file_from_zip2.html
│   │   ├──     file_from_zip3.pdf
│   │   ├──     ...
│   
├── ...
```
 
 Application does following tasks:
 
 1. Download *zip* and save it into `output_dir/zip` directory
 2. Unzip `output_dir/zip/https_www_fake_com_file.zip` into `output_dir/unzipped` directory
 3. Start iterate over files under `output_dir/unzipped` directory
 4. For every *html* or *pdf* file found in step 3. we call [HTML](#html) or [PDF](#pdf) procedure on it.
 5. If we found next zip inside base zip, we skip it.
 6. Clean `output_dir/unzipped` directory for next iteration
 
 ###### Other
 
 Other extensions are not implemented yet.
