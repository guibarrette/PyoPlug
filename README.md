# PyoPlug  

---


### Description

PyoPlug is a framework to embed the python module for digital signal processing "Pyo" into different types of audio plugins.

**Supported Wrapper**  

- VST
- Audio Unit
  
--- 

### Installation  
**Mac OS X :**  
_Make sure to have the latest Pyo build installed: <http://code.google.com/p/pyo/source/checkout>_ 

To install the plugins, compile the Xcode project or copy the compiled ones from the "Builds/MacOSX/" directory into your audio plugins folders:  

- VST : ~/Library/Audio/Plug-Ins/VST/
- Audio Unit : ~/Library/Audio/Plug-Ins/Components/

The presets are also needed to make it works. To install them, just copy the "PyoPlug" folder inside the "ScriptsPresets" folder to your Audio "Presets" folder. (This is mandatory to copy it inside the "Preset" folder of you home directory)

- ~/Library/Audio/Presets/


---    

### Documentation  
  

- PyoPlug : (Sorry, there's only a french version for now)   
	*   asdasd

- Pyo :   
	* Information: <http://code.google.com/p/pyo/>  
	* Documentation: <http://www.iact.umontreal.ca/pyo/manual/>
	* Discussions: <https://groups.google.com/forum/#!forum/pyo-discuss>


---

## Warning

The scripts are loaded directly in the Python interpreter to make it possible for Pyo to run them. This allows the importation of any Python module and scripts. This is great in a way, but can be dangereous if a script that manipulates system files or makes any unwanted behavior is loaded. Therefore, in order to avoid any problems and risks to your computer, please make sure to review any script before running it. I'm not liable to any damages of any sort and distribute this software with no warranty.

  
---

<sup>Happy coding,  
 Guillaume Barrette</sup>