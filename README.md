# RenderingModule
## Installation
### Windows
* python 3.6
* blender 2.79
* blender module
<pre>
<code>$ pip install bpy</code>
</pre>

1. Install the blender 2.79 version at https://download.blender.org/release/Blender2.79/
2. Copy <code>"C:\Program Files\Blender Foundation\Blender\\*"</code>
3. Paste into the environment folder included python.exe <code> "C:\Users\$USER NAME$\Anaconda3\envs\$YOUR VIRTUAL ENVIRONMENT NAME$" </code>

### Linux
* python 3.7
* blender 2.79

1. Download repository
<pre>
<code>$ mkdir ~/blender-git
$ cd ~/blender-git
$ git clone https://git.blender.org/blender.git</code>
</pre>
2. Download Libraries
<pre>
<code>$ mkdir ~/blender-git/lib
$ cd ~/blender-git/lib
$ svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64</code>
</pre>
3. Blender version change and update
<pre>
<code>$ git checkout blender2.7
$ git submodule update --init --recursive
$ git submodule foreach git checkout master
$ git submodule foreach git pull --rebase origin master
$ make update</code>
</pre>
4. Build blender binary
<pre>
<code>$ mkdir ~/blender-git/build_custom
$ cd ~/blender-git/build_custom
$ cmake ../blender -DWITH_AUDASPACE=OFF -DWITH_PYTHON_INSTALL=OFF -DWITH_PYTHON_MODULE=ON -DWITH_GAMEENGINE=OFF
$ make install</code>
</pre>
5. Copy and paste the specific build directory (i.e., 2.79) and dynamic library (i.e., .so) 
<pre>
<code>$ mkdir ~/blender-git
$ cd ~/blender-git/build_custom/bin</code>
</pre>
6. copy bpy.so in <code> "/home/$USER NAME$/blender-git/build_custom/bin" </code> and 2.79 directory and paste into your python 3.x/site-packages directory <code> "/home/$USER NAME$/Anaconda3/envs/$YOUR VIRTUAL ENVIRONMENT NAME$/lib/python3.7/site-packages" </code>

## Parameter
