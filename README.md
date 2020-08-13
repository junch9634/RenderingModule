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

## Rendering
<pre>
<code>python rendermodule.py</code>
</pre>

## Parameter
### Path Setting
* root_path : folder root path
* obj_path : input CAD file(obj) path
* save_path : output img path
* save_name : output img name
### Input, Output Setting
* need_normal : import and export the obj in blender(when obj has no normal information)
>  => If obj file hasn't normal information, It will raise error(Nonetype).
* size : output img size
### Camera Setting : Camera always looks at the origin.
* option : 'PERSP': perspective, 'ORTHO': orthogonal
* FOV : Camera FOV (60 is as close as possible to the assembly instructions)
* radius : Camera Location, distance from origin
* theta : Camera Location, theta(euler angle)
>  => If theta is zero, It has issue that the camera turns upside down. So when you want to 0, it is recommended to use a value that is as close to 0 as possible.
* phi : Camera Location, theta(euler angle)
### Object Setting
* obj1_location : Object location(x, y, z)
* obj1_rotation : Object rotation(x-axis, y-axis, z-axis) - Based on the axis of the object itself
* obj1_color : Object color(R, G, B)
* obj1_scale : Object scale(x, y, z)

## Result Example
<img src="/result/result.png" width="256px" height="256px" title="result example" alt="result example"></img>
