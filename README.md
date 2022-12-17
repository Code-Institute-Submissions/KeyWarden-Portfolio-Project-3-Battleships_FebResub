# Battleships
## The Plan

The plan for this project was to build a Battleships game set entirely in the console. To do this, I made the following outline:
* First, a main menu screen. This would provide the user with the options to: move the the Options screen, to start the game, or to move to the Leaderboards screen. It would also inform the user of their current settings for the game, so as to not catch them off guard.
* Second, the Options screen. From here the user would be able to change their settings. These would be the setting for the difficulty of their AI opponent (Easy, Normal, Hard), and the setting for the map size (Small, Medium, Large). They could also return to the Menu.
* Third, the Leaderboard. The idea here was that the player, after their game, would be given the option to save their score. If they chose to do so, they would be asked to input a name for the leaderboard, which would then update a Google Sheet with said name and score. By accessing the Leaderboard screen from the Menu, the player would be able to see a list of the top 10 scorse of all player in descending order, as well as their own score highlighted below, along with their place on the Leaderboard. They would also be able to view the entire Leaderboard if they so desired, and return to the Main Menu as well.
    - Note: The Leaderboard would also be the final destination after completing a game regardless of whether or not the player  saved their own score to it.
* Finally, the player could choose to start the game itself. They would then be shown an empty map of their chosen size to fill in with 5 ships (5 segment ship - Carrier, 4 segment ship - Battleship, 3 segment ships - submarine and destroyer, 2 segment ship - gunboat). The AI would also generate a random map of the same size. The player and AI would then take turns to shoot at one another until all of one side's ships were sunk, at which point the remaining side would be declared the winner.
    - The AI difficulties would specifically affect their shooting behaviour. Easy would shoot randomly even if they hit something last turn, with no strategy behind it. Normal would shoot randomly until it hit something, at which point it would fire next to that slot in a random direction until it misses, at which point it would return to random fire. Hard would fire randomly until it hits something, but would then meticulously fire adjacent to any hit marks on unsunk ships until every ship hit has been sunk, only then would it return to random fire.
    - I also had an idea for a harder difficulty that would be able to extrapolate guaranteed misses from the history of previous shots, but this idea only occured near the end, and so was cut before I could begin work on the AI.

## What was made

Unfortunately, I became over-confidant in this project, and was unable to finish more than half of it before running out of time. Of the project plan, I made the following:

* All functions controlling the Menu and Options screens were completed to the fullest extent. Only the Leaderboard screen remains unfinished.
* The Map, Ship and AI classes are almost entirely created, with only a couple of methods unfinished.
* All objects instanced from those classes are declared and appropriately labelled.
* Almost all input validation functions have been created, missing only the Leaderboard and Firing input validation methods.
* Approximately half of the work on the methods allowing the player to place their ships on their map has been completed, with most of the remaining half consisting primarily of copy-paste work that then needs minor edits to function, and the methods for the AI to do the same.

## Unfixed Bug

One "bug" I have not yet been able to remedy is that when starting ship placement you end up in an infinte loop. Most of the problem seems to simply be the parts I have not yet finished coding.

At this point there is simply nothing I can do to finish this work in even a simplified state by the deadline, and so I am submitting what I can here instead. Thank you.