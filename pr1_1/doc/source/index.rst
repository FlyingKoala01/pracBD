.. pr1_1 documentation master file, created by
   sphinx-quickstart on Mon Feb 20 09:55:25 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================
DOCUMENTATION FIRST PART LAB 1 eric hola
========================================

.. image:: upc.jpg 	
   :width: 350

This program manages the parking spots of a parking. It handles its own defined
database and permits different action to the users:

- **Occupy a parking spot**: You can choose the first parking spot available
  or input the number by yourself.
- **Leave parking**: Enter the license plate and the car will exit the spot.
- **Check parking spot availability**: It will return the license plate of
  the car that is parked there.
- **List empty parking spots**: There's a prompt for when the number of empty
  spots is bigger than 30, in order to prevent a spamming output.
- **Find vehicle in the parking**: Introduce a license plate and it will
  output the parking spot.
- **EXTRA: Show oldest vehicles**: It will show a list of license plates
  from oldest first.

The application is very robust and checks for all user inputs and database
corruption at the start of the program. It doesn't enable duplicated license
plates.

There is a single limitation in this application: **license plates must have
the "new" spanish format**. This is to ensure that they can be sorted by age.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _github-repository: https://github.com/FlyingKoala01/pracBD/tree/main/pr1_1