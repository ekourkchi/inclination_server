# Galaxy Inclination Zoo (python tools)

This repository contains the pythons codes used to manage the project server and data-base.
[Click Here](http://edd.ifa.hawaii.edu/inclination/index.php) to visit the online page of this project.

## Galaxy Inclination Zoo

​This is part of the Cosmicflows4 project to measure the distance of ~20,000 local spiral galaxies. This is a collaborative project that allows everyone interested in science to participate. The goal of this project is to find the inclination of these galaxies relative to the known standard galaxies. To achieve this goal, we offer a GUI to visually inspect these galaxies and to insert them between the standard galaxies. [Click Here](http://edd.ifa.hawaii.edu/inclination/index.php) to visit the online page of this project.


![screenshot-20180313-145248_1](https://user-images.githubusercontent.com/13570487/51081792-4f245080-169c-11e9-8bf5-3326f35f224c.png)

## Overview

The main objective of this program is to measure the inclination of a set spiral galaxies by comparing them with a number of standard galaxies. At each step, there is only one target galaxy which is displayed in a yellow panel. The inclinations of the other galaxies are known. All the standard galaxies are ordered based on their inclinations from left to right, with left galaxies having lower inclinations. User can only move the target galaxy using either the controlling left/right arrow buttons, or other methods, e.g. dragging the target panel from the middle row and replace it, or using 'A' and 'D' keys on keyboard.
To estimate the inclination of each galaxy, user goes through two steps at most. In step A, the difference in the inclination of standard galaxies is 5 degrees. Once user narrows down the approximate location of the galaxy, (s)he has the chance to increase the measurement accuracy in step B, where the inclinations are 1 degree apart. Therefore, at the end we expect users to estimate the inclination of an unknown galaxy with the accuracy of ~1 degree. Inclinations smaller than 45 degrees (i.e. galaxies more face-on than 45 degrees) would be rejected and flagged automatically and they would not be used for the distance measurement analysis. [Click Here](http://edd.ifa.hawaii.edu/inclination/index.php) to visit the online page of this project.
