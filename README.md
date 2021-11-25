# ChromePE
> Chrome Post-Exploitation is a client-server Chrome exploit to remotely allow an attacker access to Chrome passwords, downloads, history, and more.

<br />

_This script is purely for educational use. Any consequenses or damages arising from the usage of it in an illegal or unethical way are purely the fault of the end-user, and in no way is the developer responsible for it._

<br />

### Usage
#### Starting
> ChromePE is a post-exploitation tool. This means that it is meant to be placed on a victim's computer, where it will then remotely alert the attacker to more data.

**Attacker Setup**
1. ``cd path-to-chromePE/attacker``
2. ``python3 ChromePE.py``

**Target Setup**
1. ``cd path-to-chromePE/client``
2. ``python3 comm.py``

#### Attacking/Screenshots
**Attacker**
After starting the program, the attacker will be presented with a CLI and asked to select an option. 
###### Option Guide:
1. Start the Program
2. Get help (can also do when started via ``--help`` flag)
99. Exit the program

#### Credits

### License
```
Copyright 2021 Finn Lancaster

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
