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
<code>$ cd ~/blender-git/blender
$ git checkout blender2.7
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
<code>$ cd ~/blender-git/build_custom/bin</code>
</pre>
6. copy bpy.so in <code> "/home/$USER NAME$/blender-git/build_custom/bin" </code> and 2.79 directory and paste into your python 3.x/site-packages directory <code> "/home/$USER NAME$/Anaconda3/envs/$YOUR VIRTUAL ENVIRONMENT NAME$/lib/python3.7/site-packages" </code>

## Rendering
<pre>
<code>python rendermodule.py</code>
</pre>
You can set parameters in 'rendermodule.py'
<pre>
<code>python rendermodule.py --json YOUR_JSON_FILE_PATH</code>
</pre>
You can set parameters by JSON file

## JSON(INPUT)
    setting = {'object': [
        {'name': name1,
         'location': obj1_location,
         'rotation':obj1_rotation,
         'color': obj1_color,
         'scale': obj1_scale
         },
        {'name': name2,
         'location': obj2_location,
         'rotation': obj2_rotation,
         'color': obj2_color,
         'scale': obj2_scale
         }
        ],
        'camera': {
            'option': option,
            'fov': FOV,
            'radius': radius,
            'theta': theta,
            'phi': phi
        },
        'input': {
            'part': part
        },
        'output': {
            'size': size
        },
        'path': {
            'root_path': root_path,
            'obj_path': obj_path,
            'save_path': save_path,
            'save_name': save_name
        }
    }

**You can see detail example in 'rendermodule.py'**

## Parameter
### Path Setting
* root_path : folder root path
* obj_path : input CAD file(obj) path
* save_path : output img path
* save_name : output img name
### Input, Output Setting
* part : rendering mode according to '0' = furniture part, '1' = connector part
>  => You can change rendering detail at declare the freestyle_info
* size : output img size
### Camera Setting : Camera always looks at the origin.
* option : 'PERSP': perspective, 'ORTHO': orthogonal
* FOV : Camera FOV (60 is as close as possible to the assembly instructions)
* radius : Camera Location, distance from origin
* theta : Camera Location, theta(euler angle)
>  => If theta is zero, It has issue that the camera turns upside down. So when you want to 0, it is recommended to use a value that is as close to 0 as possible.
* phi : Camera Location, theta(euler angle)
### Object Setting
* name : obj file name (X.obj)
* obj_location : Object location(x, y, z)
* obj_rotation : Object rotation(x-axis, y-axis, z-axis) - Based on the axis of the object itself
* obj_color : Object color(R, G, B)
* obj_scale : Object scale(x, y, z)


## Result Example
<img src="/result/result.png" width="256px" height="256px" title="result example" alt="result example"></img>
<img src="/result/result2.png" width="256px" height="256px" title="result example" alt="result example"></img> 

<img src="/result/result3.png" width="256px" height="256px" title="result example" alt="result example"></img>
<img src="/result/result4.png" width="256px" height="256px" title="result example" alt="result example"></img>


# Issues
* 체결 부품(connector part) Rendering시, 대회측에서 제공받은 CAD 파일이 조립설명서상의 체결부품과 동일하지 않아(ex. 나사선) 렌더링된 이미지가 조립설명서와 차이가 있을 수 있습니다.
* 가구 부품과 체결부품의 rendering 할 시에 선 굵기 등의 디테일이 달라 part=0, 1로 분리시켰습니다.
<img src="/issue/Assembly_instruction.jpg" title="Assembly instruction" alt="Assembly instruction"></img>
<img src="/issue/stefan_obj.png" title="stefan obj" alt="stefan obj"></img>

