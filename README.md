# Delete unused media files from Django project

This package provides management command `cleanup_unused_media` for Django applications. With 
help of this management command you can remove all media files which are no longer used (files 
without references from any Django model with `FileField` or `ImageField` fields or their 
inheritances). The files will be placed in the quarantine folder before it is removed. 

# Installation

1.  Install ``django-unused-media``; copy the folder `django_unused_media` into the root dir of 
your Django project. 

    Python 2.7, 3.6, 3.7 are tested with tox.
    
    Django 1.8, 1.9, 1.10, 1.11, 2.0, 2.1 are tested with tox.

2.  Add ``django-unused-media`` to ``INSTALLED_APPS``:
    ```python
    INSTALLED_APPS = (
        ...
        'django_unused_media',
        ...
    )
    ```

# Usage

To cleanup all unused media files, run management command:
```
./manage.py cleanup_unused_media
```
By default command is running in interactive mode. List of files which are going to be placed in 
quarantine will be displayed for confirmation. User have to confirm the action.

### Options

#### `--noinput`, `--no-input`

Non interactive mode. Command will remove files without any confirmation from user. Useful for scripts.
```
./manage.py cleanup_unused_media --noinput
```

#### `-e`, `--exclude`

To avoid operating on particular files you can use exclude option. 
- *`*` as any symbol is supported.*
- *Can use multiple options in one command.*

For example, to keep `.gitignore` and `*.png` files you can use:
```
./manage.py cleanup_unused_media -e *.gitignore -e *.png
```

Also you can exclude entire folder or some files in that folder (path should be relative to `settings.MEDIA_ROOT`):
```
./manage.py cleanup_unused_media -e path/to/dir/* -e path/to/dir/my*.doc
```

#### `-i`, `--include-models`

To avoid operating on particular files you can use the include option. Unlike the exclude option 
this option make sure that only the included models are processed. For the supported models see 
the documentation of the `--show-possible-models` option.
- *Can use multiple options in one command.*

For example, to only process the `files` and `user` models:
```
./manage.py cleanup_unused_media -i files -i user
```

#### `-m`, `--show-possible-models`

This show a list of all the models that contain a field which is a instance of FileField.

#### `--remove-empty-dirs`

By default script keep empty dirs in media folder. But with this option empty directories will be removed after cleaning process automatically.

#### `--dry-run`

Dry run without any affect on your data

#### `--verbosity {0,1}`, `-v {0,1}`

Verbosity level. 0 - minimal output, 1 - normal output (default)

#### `-c`, `---cleanup_quarantine`

Removes files that have been 90 days or longer in quarantine.

# Tests
At first make sure that you are in virtualenv.

Install all dependencies:
```
make setup
```
To run tests:
```
make test
```
To run static analyser:
```
make flake8
```

# Acknowledgements

This project is a fork of [akolpakov](https://github.com/akolpakov/django-unused-media), this 
project has an opt-in feature and places the files in quarantine first for cleaning up unused media 
files.

# License
[MIT licence](./LICENSE)