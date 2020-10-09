# Developer Documentation (work in progress....)
This document is for developers who want to create a third-party module for the Inkycal project

## Getting started
To get started, copy the [template file](https://github.com/aceisace/inkycal_template/blob/master/mymodule.py) into the modules folder:

```bash
cd Inkycal/inkycal/modules
wget https://raw.githubusercontent.com/aceisace/inkycal_template/master/mymodule.py
```

All inkycal modules are classes with 3 inherited functions:
* the `__init__` function, which allows loading config, setting options etc. (does require changing)
* the `set()` function, which allows changing options (does not require changing)
* the `generate_image()` function. This is where all the code should be to generate the image for your module


## Rename file and Class
* Rename the file `mymodule.py`.
Please keep in mind to use only lowercase and preferably a not-too-long name and without numbers.
Do not give it a name that conflicts with any built-in libraries or any libraries that will be used by the module.

| Good examples | Bad examples |
| -- | -- |
| `weatherwarning.py` | `calendar.py` (a built-in library is also called calendar!) |
| `current_traffic.py` | `HelloWorld` (use only lowercase!) |
| `hello_world.py` | `weather2.py` (do not use numbers!) |

* Rename the class
Classnames start with a __Capital__ letter, do not contain numbers or special symbols.

| Good examples | Bad examples |
| -- | -- |
| `Weather` | `simple` (class names should start with a capital letter!) |
| `Location` | `Weather2` (no numbers in classname!) |
| `Weatherwarnings` | `Someverylongname` (Imagine having to type this 100 times! It's too long!) |

## Think about the required config
What do you need from the user to run your module?
Which options should the user have access to for customizing?

Once you have a rough idea of these, create a config section for your module by changing the end of the file from this:
```
if __name__ == '__main__':
  print('running {0} in standalone mode'.format(filename))
```

to something like:

```
if __name__ == '__main__':
  print('running {0} in standalone mode'.format(filename))
  section_size = (480, 200)
  
```




