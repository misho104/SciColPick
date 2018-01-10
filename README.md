SciColPick
==========

A (**alpha version**) color-palette generator for scientific plots.
The colors are friendly to monochrome printers (and thus to color vision deficiency).


### Set up

#### Environment

Python 3

#### Install

```console
$ pip install git+https://github.com/misho104/SciColPick.git
```

or you can install specific version by, e.g.,

```console
$ pip install git+https://github.com/misho104/SciColPick.git@v0.1.0       # for v0.1.0
$ pip install git+https://github.com/misho104/SciColPick.git@development  # for development version
```

#### Upgrade

```console
$ pip install git+https://github.com/misho104/SciColPick.git --upgrade
```

#### Uninstall

```console
$ pip uninstall SciColPick
```


### Usage


```sh
SciColPick 4   # and exit with CTRL+D (or CTRL+C)
```
or any numbers (but should be smaller than 10).

The code first generates a gray-scale palette, which is optimized so that the color distances among the grays are maximized. Then the code trys to give random colors to the palettes to maximinze the quality, which is defined by the minimum distance among the colors.

Two files are generated in the same directory: `result.png` shows the best color palettes:
![result.png](https://user-images.githubusercontent.com/776101/34788602-5c9d054a-f63b-11e7-86ad-af8c5cbae578.png)

The top color is the grayscaled version of the palettes, which is common to all the color palettes. Lower color palettes have better quality.

`result.txt` includes the HEX color information.

```result.txt
Gray scale: #000000 #383838 #646464 #8a8a8a #bdbdbd #ffffff 
Color No.0: #000000 #1b3864 #714ebf #cb60ce #c8baae #ffffff   (d=16.727270977014992)
Color No.1: #000000 #531286 #4249fa #449e00 #d6afe7 #ffffff   (d=20.0369135457199)
Color No.2: #000000 #601b57 #3e57d7 #c856f6 #e1b39b #ffffff   (d=22.47966195861073)
Color No.3: #000000 #2d2396 #107346 #a0866d #61cfb4 #ffffff   (d=27.980555645714265)
Color No.4: #000000 #4f1686 #815d36 #6390a9 #71d185 #ffffff   (d=29.178018680206794)
Color No.5: #000000 #5d0b7b #915448 #fb25be #47d48f #ffffff   (d=29.89889687321007)
Color No.6: #000000 #402187 #9b4c4e #9978e2 #87cf56 #ffffff   (d=30.232839280322793)
```


### Author

Misho
