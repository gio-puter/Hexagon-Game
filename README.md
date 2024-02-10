# [Hexagram](https://hexagram.glitch.me)
## Idea
This game is a subset of the nonogram games, but with a hexagon layout.
This means that the user gets clues on the three open sides of the hexagon tessellation.
The tessellation setup alternates column height and is created so that the number of clues is the same on all three sides.
This means that we can get tessellations denoted by their columns as so: 3-4-3-4-3 and 4-5-4-5-4-5-4.

# Example:

Hints:

<img width="750" alt="Screen Shot 2023-09-17 at 1 41 14 PM" src="https://github.com/gio-puter/Hexagon-Game/assets/103840942/0cab93a8-ee54-4b13-9185-bdea0492f750">

Possible Solution:

<img width="750" alt="Screen Shot 2023-09-17 at 1 42 14 PM" src="https://github.com/gio-puter/Hexagon-Game/assets/103840942/1784a132-7711-4abc-a170-e01f5983d356">

# Current State and Future
Right now, I have written some scratch code in Python using the tkinter module for what I imagine this game would look like.
This code automatically creates the hexagon layout as shown in the example and randomly chooses the clue numbers.
This will eventually transition to code written in JavaScript, HTML, and CSS.

This is a small project, but I still need help with some things:
1) Though it's scratch code, cleaning some of it up and optimizing it would go a long way in making the transition to web programming much smoother.
2) If you read the code, you'll notice that I have a specific way of writing the rows and columns due to the hexagon grid layout. If you have a better, clear, more efficient way of creating the grid and/or checking that the user solution is correct, let me know.
3) Any work on the JavaScript, HTML, and CSS would help tremendously. I'm not very good at HTML and CSS so anything there to replicate a look similar look to the example is awesome. This also inclues any UI suggestions to make things clearly (such as adding arrows next to the clues to indicate what they are addressing).
4) ~~The user should be able to mark a cell as ineligible with a right mouse click which should prevent them from coloring it in unless they unmark it.~~ Ok I added this. But it definitely could be better. I'm open to suggestions.

Look at other nanograms (such as http://liouh.com/picross/) for inspiration in how things should generally work.


Thank you for any help or ideas you may be able to provide.

\- Gio
