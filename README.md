
 PyGitLatex
============

Author: Andrew S. Wixom

Introduction
------------

The goal of this project is to provide a simple interface
enabling collaboration between authors of a Latex document
using Git. To some extent, this is an already solved 
problem: see the excellent ShareLatex/Overleaf software.
And, further, it should be noted that PyGitLatex is **not**
a replacement for ShareLatex/Overleaf. However, for some
users (meaning at least the author) the ShareLatex/Overleaf
framework has a few disadvantages. PyGitLatex aims to 
correct these by providing the following features:

- Direct control of project history (i.e. git respository)
- Allowing the user's preferred/existing Latex toolchain
- No required cloud-based storage or computing

To do so, PyGitLatex provides a simple graphical interface
including some of the basic features of both Git and Latex.
Advanced users of either software are free to make changes 
using whatever toolchain they are familiar with. History
will be tracked through a standard Git repository and 
therefore may be manipulated using any appropriate 
commandline or GUI either alongside or instead of PyGitLatex.
Similarly, the goal is to require no particular Latex 
packages, settings, or editor/viewer. The only constraint
is that all collaborators on a particular project are 
familiar enough with their chosen environment to compile
the package independently. 

Installation
------------

PyGitLatex requires three main softwares to be installed 
on a user's computer, all three of which are available on 
all popular operating systems although at times under 
slightly different names.

  - Python3 interpreter with the following packages:
      + pyforms 
      + gitpython
  - Git
  - Latex

Once these have been installed, PyGitLatex may be run by
invoking the python3 interpreter on the python script in 
this repository.

At some point in the future, self installer packages may
be provided.

User's Guide
------------

... will be included later...


