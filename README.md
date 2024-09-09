# Root-Access

## About

Root Access is a system That interfaces a raspberry pi with an arduino to autonomously grow a plant by reading input from a temperature, humidity, moisture, light, and
float sesnors and responding accordingly to accomodate the best growing conditions for the plant (in our case, reb rubin basil). This project sought to answer 2 questions:

1. How well does a computer grow a plant on its own?
2. Does the resource consumption (water, electricity) "cost" justify automating plant growth in a controlled environment vs taking care of them by hand?

To grow the plant, we have hardcoded inflection points (in arduinoDriver.py) that the process reacts to. For example, If the ambient light level falls below 100,
turn the lamp on. We found our inflections points through trial and error by hooking our sensors up and outputting our sensor data to the terminal, and deciding "Yep,
it's too dark, 100 seems like a good spot to turn the lights on" or "the soil seems moist enough to me, let's make sure it tries to maintain this moisture." In a future
iteration of Root Access, in a system of thousands of plants, hooked up to cameras to capture the plant's growth autonomously, a machine learning model could be
implemented to determine the best values.

As it turns out, our guesstimations weren't bad at all. To test our system, we did an experiment. The 3 of us (Jon Martin, Wesley Elliot, and Eric Webb) each took a
flower pot, planted a seed, and watered it on a set frequency on the same window sill where our autonomous system was to compare the growth results and resource usage.
For good measure, we also set up the same hardware to run off of a timer to water the plant and turn the lamp on in set intervals. While each of us maintained a set
schedule to water our plants, we watered as frequently as we assumed out plant needed it. I (Eric Webb) for instance watered it every day, while Jon and Wesley watered
theirs less frequently. The experiment ran for 6 weeks, by the end of which, the autonomous systems were the only ones with living basil. The "reactionary" system used
much less electricy and water than the timer system, which used way less water than any of the 3 of us used. The reactionary system also used less electricity than the
timer system, and the basil grew a few inches taller in that time. Granted, this was a small experiment in the grand scheme of things. That said, the results were very
exciting, as the possibility to set up the reactionary system with a solar panel anywhere in the world was discovered to be feasible rather than fantasy

[**Forked from here**](https://github.com/root-access-capstone)
