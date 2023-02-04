# Battleships

Battlships is a simple game played entirely in the console, based on the original Battleships, a board game played by many even to this day. It is single player, with the player playing against an AI opponent. The goal of the game is to simulate the Battleships experience as closely as possible.

The game itself is targeted both towards people who want a simple but fun experience, as well as towards those with strong memories of the original experience it is based on.

## Features

### Implemented

* __Menu__
    * A fully functional Menu system prior to game start. This allows the player a degree of control over their experience, and contains multiple screens to facilitate this.
        * First, is the Main Menu, which is the first Menu seen by the user and allows them to start the game immediately if they should so desire. It also allows them to access the Options Menu to customise the difficulty of the AI and the size of the grid they will be playing on. It also provides access to the Leaderboard (more on this later), as well as the ability to view the Instructions for the game.
        * Second, the Options Menu. As mentioned above, this Menu allows the user to alter the difficulty and map size of their play session before properly starting the game, and send them to one of two Sub-Menus: Difficulty and Map Size. The user can also return to the Main Menu from here.
            * The Difficulty Sub-Menu allows the user to adjust the AI difficulty between one of three options: Easy, Normal, and Hard. The specifics will be covered in the "AI" subsection of the Implemented section of this document. The user can also return to the Options Menu proper from here.
            * The Map Size Sub-Menu allows the user to adjust the size of the grid they will play on between one of three options: Small, Medium, and Large. The specifics will be covered in the "Grid" subsection of the Implemented section of this document. The user can also return to the Options Menu proper from here.
* __Leaderboard__
    * As mentioned in the "Menu" subsection abover, the Leaderboard can be accessed from the Main Menu. Here, the user is presented with a list of saved scores from prior users, as well as the AI difficulty they played on, sorted in descending order based on their scores.
        * This allows the user to not only see the kinds of scores that are possible to acquire in the game, but also the ability to compare their own score(s) against them, especially if they should choose to save them directly to the Leaderboard (more on this later).
        * The Leaderboard itself is actually stored on a seperate Google Sheets Document that the program can access and update under specific conditions, with the Document automatically sorting itself everytime the date within is updated.
* __Game__
    * The Game itself is, much like the Leaderboard, launched from the Main Menu. Contained within is the full gaming experience of Battleships, in the proper order: Ship Placement, Firing, Ending, and Score Submission. This allows the user to experience a game of Battleships to its fullest.
        - _Ship Placement_ - Here, the user is shown their grid or 'map', containing as many ships as they have currently placed, starting at none by default. The user is then asked to place their ships in the following order: Carrier (length of 5 spaces), Battleship (length of 4 spaces), Destroyer (length of 3 spaces), Submarine (length of 3 spaces), and Gunboat (length of 2 spaces). The grid updates as they are placed.
            - Before placing, the user is provided the option to rotate the ships. They default to horizontal (left to right) alignment, but can be rotated to vertical (top to bottom) and back again as the user wishes.
            - When placing, the user is asked to enter the grid coordinates (collumn, row) of where they wish to place either the left-most or top-most section of the ship, depending on orientation. Assuming the input is valid (within the bounds of the grid, not taken already, not too close to an already taken space, and not too close to either the right or bottom edges depending on orientation), the grid will update as appropriate, and the user moves onto the next ship.
            - Grid spaces taken by your ships will be represented with an '@' symbol.
            - The AI will also have a grid, which will be generated randomly.
        - _Firing_ - Here, the user and the AI will take turns to fire shots at eachother's grids, with the first turn being assigned randomly. The user will be shown an empty grid of appropriate size, representing the enemy's grid, with no ships filled in yet, so as to avoid telling the user exactly where to shoot.
            - In order to fire, the user will be asked to enter the coordinates of the grid they wish to shoot. Assuming the input is valid (within the bounds of the grid, and not a previously shot space), the user will then be told if they scored a Hit or a Miss.
                - If the user score a Hit, it will be represented with an '#' symbol in the appropriate space of the grid. They will also be awarded 10 points.
                - If the user Misses, it will be represented with an '~' symbol in the appropriate space of the grid. They will also lose 1 point.
                - If the user sinks a ship, they will be informed, and will be awarded an additionaly 100 points
            - Information on how the AI chooses a space to shoot will be covered in the "AI" subsection of the Implemented section of this document.
        - _Ending_ - Here, once either all the user's or all the AI's ships are sunk, the game begins the ending process. The user is first informed of either the Victory or Defeat, and told their score. Should they have won, they will also be provided the option to save their score to the Leaderboard (more on this later). Finally, they will be provided with three options to proceed.
            - First, to start the game again. This will skip the Menus entirely, and start the game proper again with the same difficulty and map size settings.
            - Second, to return to the Main Menu. As described in the name, this option returns the user to the Main Menu proper, just like if they started the entire program over.
            - Third, to see the Leaderboard. This lets the user immediately compare their score to past users.
        - _Score Submission_ - This is only seen if the user both wins, and chooses to save their score. Here, they are asked to implement a username to be assigned to their score. In keeping to the Arcade feel of playing a game set entirely in the console, the usernames are limited to three characters in length, though whitespace is not allowed.
* __AI__
    * As mentioned above, the AI comes in three difficulty options: Easy, Normal, and Hard. The user is granted full control over which they wish to face. This allows the user to customise how challenging an experience they wish to face. The user will lose 5 points every time one of their ships is hit, and will lose 50 every time one of their ships is sunk.
        * _Easy_ - At Easy level, the AI will always choose its shots randomly, and will never adjust this strategy even if it lands a hit. This provides a very casual experience for the user, where victory is very likely, and defeat something the user would need to work to experience.
        * _Normal_ - At Normal level, the AI will adjust its strategy on landing a hit, randomly choosing a direction from that space and firing at the adjacent space in that direction on its next turn. However, upon missing it will return to random fire. Defeat is now plausible, though luck continues to play a heavy role in winning or losing.
        * _Hard_ - At Hard level, the AI will adjustits strategy on landing a hit. It will begin a meticulous process of methodically shooting in a given direction each turn until either the ship it hits has sunk or it misses. If it misses, it will return to the first space it shot and begin the process again in a different direction, continuing until the ship is sunk. At this level, each hit will inevitably result in a sunken ship given time. This process works of a predictable pattern, however, so if the user learns it, they can determine how much longer that ship has until it is sunk. Defeat is now not just plausible, but considerably believable.
* __Grid__
    * As mentioned abover, the Map Size comes in three options: Small, Medium, and Large. The user is granted full control over which size they want the grids to be. This allows the user to customise how long they want each game to go on. Small grids tend to result in fast games, where has Large grids can plausible take up to an hour in the extreme cases.
        * _Small_ - 10 x 10
        * _Medium_ - 15 x 15
        * _Large_ - 20 x 20

### Dropped

* __AI__
    * Originally I had planned on making the Hard AI follow the same meticulous process until every hit space they found became part of a sunken ship, but due to time constraints I was forced to drop this option. As is, I now think it would serve well in the future as a Hard+ or Harder Difficulty option.
    * I had an idea at one time for a Hardest Difficulty option, where the AI would ignore grid spaces where it is physically impossible for a ship to be found when firing, much like how a person would. Much like the Hard+ option, this had to be dropped due to time constraints.
    * A Final AI related idea I had was for an Extreme Difficulty. Here, the AI would follow the next highest option when firing, but every so often would fire a shot guaranteed to hit one of the user's ships. The exact timeframe this would occur in was never narrowed down, as this option was cut due to feeling too unbalanced in concept, as it would likely be frustrating to fight against.
* __Grid__
    * I debated including larger and smaller map size options then the ones provided, but eventually chose to settly for those already present. Large is already sufficient in size as to occasionally cause problems (more on this in the Known Bugs section), and Small is at just the right size to provide a quick but fun experience without risking either the user or the AI accidentally bricking their ability to place further ships in the Ship Placement stage.

## Testing

### Completed Testing

I tested the program extensively in order to remove any bugs or issues I could find. This consisted of both running the functions directly with practice values, and even playing the full game, as well as using the CI Python Linter Validator.

While testing I encountered a variety of minor bugs and issues that were swiftly resolved. Most were merely typos, although a more significant error I encountered resulted in me relearning about how Python will assume a variable is local - even when it shares the same name as a global variable - if you assign anything to it within a function without including 'gobal (variable_name_here)' at the top of the function.

I can now confidantly say that the program, when run through the CI Python Linter Validator, returns no errors.

### Unfixed Bugs

There are only two unfixed bugs I have ben unable to resolve, primarily because I cannot identify how they are occuring in the first place.
* The first occurs when placing ships, occasionally, and seemingly only when placing the Submarine and after inputing an invalid value. The function for controlling which spaces are invalid when will return an error. I currently do not have an explanation for this issue.
* The second occurs when playing on Large grids. For reasons unknown, the grids will occasionally simply not print durin the Firing stage of the game. The reason for this is unknown as the code to print the grids is fully implemented, and the rest of the game continues to run as though the grids were printed.

## Sources

I copied the code for connecting the program to the Google Sheets API from the love sandwiches project.

## Deployment

* The site was deployed to GitHub pages. The steps to deploy are as follows:
    - In the GitHub repository, navigate to the Settings tab
    - From the source section drop-down menu, select the Master Branch
    - Once the master branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.
