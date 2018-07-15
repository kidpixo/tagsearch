## Sales pitch

At the top of the Readme, explain very succinctly

1) what the project does
2) why you should use it.

The first point forces you to be clear about what you’re building.  The second
point forces you to justify why you’re building it and not, for example, using
a library already in your code base, or an open source library, or building
something else entirely (see “Build in-house, buy commercial, or use open
source”). If you can’t justify why someone should use it, you probably
shouldn’t build it.

## Examples

After the sales pitch, show a few code snippets, UI mockups, screenshots, or
architecture diagrams, that demonstrate how to use the project.
This is your chance to figure out the user experience up front.

Many programmers, unfortunately, skip this step and go straight into the
implementation. They start fighting with the trickiest bit of code and pile on
layer after layer on top of it. Slowly, like a weed crawling up a tree in a
jungle, they wind their way up and up, until at some point, they break through
the canopy, and for the first time, expose their code to the sunlight—that is,
to real users. Whatever mess happens to be at the edge of this tangle of weeds
becomes the user experience. In most cases, this API or UI is completely
unusable, but by now, it’s too late to fix it because there are too many
branches, roots, offshoots, and code to make a meaningful change.

That’s why you should start with the user experience first (see Chapter 3).
It’s often both the hardest part of the project and the one that most
determines if the project will be successful.  

## Quick start guide

You’re not done thinking about the user experience yet. After you list a few
examples, the next step is the quick start guide, where you explain how to
install the project and start using it. This will force you to think about how
your project will be packaged, what dependencies it has, what kind of
configuration it needs, and how it will work in both development and production
environments. Do not put these decisions off until the end.
They are an integral part of the experience of using your product and they
always take longer to get right than you expect.

One of my favorite examples is to compare the quick start guide for building a
simple web app on the Spring Framework versus Node.js. The tutorial for Spring
takes 15 minutes (if you don’t make any mistakes) and includes a dozen steps
where you create 8 folders and files and write 88 lines of code (yes, I
counted) across 2 programming languages.
With Node.js, it takes 2 steps and 15 seconds: you copy and paste 6 lines of
code from the Node.js homepage into a single file on your computer, and run
it. Is it a surprise that Node.js is one of the fastest growing open source
projects of all time? The quick start guide is your first impression. Make sure
you get it right.

## Project organization

This is the section where you explain the mechanics of working on this project.
Where does the code live? How is the code organized? How are tasks and bugs
tracked? How do you contribute? What are the legal considerations (license,
copyright)? If you want to be able to work on this project with other people,
it’s essential to figure out these administrative details ahead of time.

