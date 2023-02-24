.. pr1_2 documentation master file, created by
   sphinx-quickstart on Mon Feb 20 09:55:25 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================
DOCUMENTATION SECOND PART LAB 1
===============================

.. image:: upc.jpg 	
   :width: 350

This program manages the parking spots of a parking. It handles its own defined
database and permits different action to the users:

- **Occupy a parking spot**: You can choose the first parking spot available
  or input the number by yourself.
- **Leave parking**: Enter the license plate and the car will exit the spot.
- **Check parking spot availability**: It will return the info of
  the vehicle that is parked there.
- **List empty parking spots**: There's a prompt for when the number of empty
  spots is bigger than 30, in order to prevent a spamming output.
- **Find vehicle in the parking**: Introduce a license plate and it will
  output the parking spot.
- **List vehicles of specified brand/color**: It will show a list of the
  vehicles that mach the user's requirements.

The application is very robust and checks for all user inputs and database
corruption at the start of the program. It doesn't enable duplicated license
plates.

**EXTRA:** This second part is fully object-oriented. Check the modules
to see how clean the code looks!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
