# TinyPlusPlus-Compiler
This is a simple compiler made with educational ends.

Were applied each of the phases of the compiler development basis (lexical, syntax, semantic and runnable code generation).

__How to install:__
The compiler has been made with the idea to use a compilation in the command line prompt to let the users include their own IDEs or some tool to simplify the compilation process.
The steps to run any tinypp code are this:
*Step 1:*
Download or clone the tiny project. (Obviously gg)

*Step 2:*
Navigate to TinyPlusPlus-Compiler/tinypp folder and add this absolute path to the environment variables with the name "tiny".

*Step 3:*
All is done, now you can write some tinypp program and run it.

*To compile code:*
> tiny <thename of your file>
Note: The file can have any extention (.txt, .code, etc) but I suggest to use .tiny, because is cool.

This compilation will generate a couple of files, the most important file is "code.tm", this is the runnable code.

*To run:*
> tinym code.tm
The tinym is like a simple virtual machine to run the kind of code generated with the tinypp compiler.



__Syntax of the tinypp language:__
The language is really "tiny" and it can't do too much more than simple mathematical programs.

*Program structure:*
*
main {
  <variable declarations>
  <body of the program>
}
*

*Supported data types:*
int, real & boolean.

*Supported math operations:*
Multiplication (*), Division (/), Addition (+), Substractions (-).

*Supported logical expressions:*
>, <, >=, <=, ==, !=

*Asignation symbol:*
:=

*Input and output:*
cout <any expresion, variable or constant>;
coutln <any expresion, variable or constant>;
coutln; //This is to generate a single jump line
cin <some variable>;

*Flow control:*
if(<boolean expression>) then {
  <true body>
}
else {
  <false body>
}

*Loops:*
while(<boolean expression>) then {
  <body>
}

repeat {
  <body>
} until(<inverted boolean expression>);


__The IDE:__
I've also made a simple IDE made with C#, it doesn't has a lot of science, is located under TinyPlusPlus-Compiler/Libre-IDE, just run it from the debug folder of the .net project, open a tiny file, and press the green button to compile and run the code.

And that's it. As you can see I don't implemented characters or strings handling, so it limits a lot the language capabilities, but as I previously said, this is for learning ends.
