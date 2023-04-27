# **Regular Expression to DFA Conversion in Compiler Design**
The purpose of this project is to develop a tool that converts regular expressions into deterministic finite automata (DFAs) for use in the lexical analysis stage of compiler design.The lexical analysis stage is the first step in the compilation process, where the input source code is broken down into a sequence of tokens that are used by the compiler to further analyze the code. Regular expressions are commonly used to describe the patterns of characters that make up the tokens in a programming language. The tool will take a regular expression as input and output a DFA that can recognize the language described by the regular expression. The conversion process involves several steps, including converting the regular expression into it's postfix notation, from the postfix notation create syntax tree, from the syntax tree calculate nullable, firstpos, lastpos, followpos for each nodes and from here create the dstate table (DFA transition table) which will lead us to the required DFA.
<br />

##### **This project was a part of my undergraduate course CSE420 (Compiler Design)**
---

## **Language used**
* Python
