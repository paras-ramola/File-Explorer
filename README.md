<h1>NAVI Explorer</h1>

<p><strong>NAVI Explorer</strong> is a cross-platform file explorer developed as an Operating Systems mini project. It features a graphical interface built using Python (Tkinter) and a command-line interface written in C (using ncurses), supporting essential file operations and user roles.</p>

<h2>Features</h2>

<h3>Graphical User Interface (GUI)</h3>
<ul>
  <li>Guest and Administrator login modes</li>
  <li>Dark-themed modern interface</li>
  <li>Create, rename, delete, and copy files and folders</li>
  <li>Real-time directory search</li>
  <li>Sorting by name, type, size, or modification date</li>
  <li>Navigation history and recent files</li>
  <li>Quick access to system folders (Desktop, Documents, Downloads, etc.)</li>
  <li>Grid-based layout with icons</li>
</ul>

<h3>Command-Line Interface (CLI)</h3>
<ul>
  <li>Ncurses-based terminal UI</li>
  <li>Arrow-key navigation</li>
  <li>Open, rename, and delete items</li>
  <li>Cross-platform support (Linux, macOS, Windows via WSL)</li>
</ul>

<h2>Project Structure</h2>

<pre>
navi-explorer/
├── front.py           # Main login interface
├── admin.py           # Administrator file explorer
├── guest.py           # Guest (limited access)
├── cli_explore.c      # CLI (ncurses-based)
├── images/            # Icon assets
│   ├── blank_dp.jpg
│   ├── folder_icon.png
│   ├── file_icon.png
│   └── app_icon.png
└── README.md
</pre>

<h2>Installation</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.7 or higher</li>
  <li><code>tkinter</code> and <code>pillow</code> packages</li>
</ul>

<pre><code>pip install pillow</code></pre>

<p>For CLI:</p>
<ul>
  <li>Linux/macOS: ncurses (usually pre-installed)</li>
  <li>Windows: Use WSL (Windows Subsystem for Linux)</li>
</ul>

<h3>Setup</h3>
<ol>
  <li>Clone or download the project</li>
  <li>Ensure all images are inside the <code>images/</code> folder</li>
  <li>Compile the CLI:
    <pre><code>gcc -o cli_explorer cli_explore.c -lncurses</code></pre>
  </li>
  <li>Run the GUI:
    <pre><code>python front.py</code></pre>
  </li>
</ol>

<h2>Usage</h2>

<h3>Login Modes</h3>
<ul>
  <li>Guest Mode: Basic browsing</li>
  <li>Admin Mode: Full access (default password: <code>1234</code>)</li>
</ul>

<h3>GUI Controls</h3>
<ul>
  <li>Click to enter folders</li>
  <li>Use the Back button to navigate history</li>
  <li>Right-click for file actions</li>
  <li>Sidebar: Create and sort items</li>
  <li>Search bar: Filter results</li>
</ul>

<h3>CLI Controls</h3>
<ul>
  <li><strong>Arrow Keys</strong>: Move up/down</li>
  <li><strong>Enter</strong>: Open selected item</li>
  <li><strong>R</strong>: Rename</li>
  <li><strong>D</strong>: Delete</li>
  <li><strong>Q</strong>: Quit</li>
</ul>

<h2>Customization</h2>

<h3>Change Admin Password</h3>
<p>Edit the following in <code>front.py</code>:</p>
<pre><code>def verify_admin(pswrd):
    if pswrd == "YOUR_NEW_PASSWORD":
</code></pre>


<h3>Add System Folders</h3>
<p>Edit <code>SYSTEM_FOLDERS</code> in <code>admin.py</code>:</p>
<pre><code>SYSTEM_FOLDERS = {
    "Root": os.path.abspath(os.sep),
    "Home": HOME,
    "Custom": "/path/to/folder"
}
</code></pre>

<h2>Platform Compatibility</h2>

<table border="1" cellpadding="4" cellspacing="0">
  <tr>
    <th>Platform</th>
    <th>GUI</th>
    <th>CLI</th>
  </tr>
  <tr>
    <td>Windows</td>
    <td>Yes</td>
    <td>WSL or compatible terminal</td>
  </tr>
  <tr>
    <td>Linux</td>
    <td>Yes</td>
    <td>Yes (native)</td>
  </tr>
  <tr>
    <td>macOS</td>
    <td>Yes</td>
    <td>Yes (native)</td>
  </tr>
</table>

<h2>Troubleshooting</h2>

<ul>
  <li><strong>Images not loading</strong>: Ensure image files are in the correct folder</li>
  <li><strong>Permission denied</strong>: Run with appropriate user permissions</li>
  <li><strong>CLI not working</strong>: Ensure ncurses is installed or use WSL</li>
  <li><strong>File errors</strong>: Verify file paths and check disk permissions</li>
</ul>

<h2>Development</h2>

<ul>
  <li><strong>front.py</strong>: Entry point and login logic</li>
  <li><strong>admin.py / guest.py</strong>: GUI features</li>
  <li><strong>cli_explore.c</strong>: Terminal-based navigation</li>
</ul>

<p>Code is written using modular functions and object-oriented design where applicable. Error handling and cross-platform compatibility are built in.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<pre>
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
</pre>

<h2>Contributions</h2>

<p>Contributions are welcome. Please submit issues or pull requests on the repository for bugs and feature suggestions.</p>

<h2>Acknowledgments</h2>

<ul>
  <li>Developed using Python (Tkinter) and C (ncurses)</li>
  <li>Designed for educational use in Operating Systems coursework</li>
  <li>Icons and layout optimized for usability and clarity</li>
</ul>
