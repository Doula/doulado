==================================
 Dould Build and Deployment Tools
==================================

This could have been called *fertilize*.


Purpose
=======

This repository will attempt to act as the single point of departure
for code that builds and deploys doula and related projects.


Dev Install
===========

If you would like to hack on doula, `doulado` provides a command for
installing all the dependencies you might need::

 <in side an activated virtualenv> 
 pip install -e git+git://github.com/Doula/doulado.git#egg=doulado
 doula devinst


Service creation
================

`doulado` provides a mechanism to create a service within a site
environment. This means the creation of the following::

 * a master package repo 
 * a configuration repo
 * an application state repo

 



