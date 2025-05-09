# Analyze the Messier Catalog

In this assignment, you will practice using logic and loops using a dataset of objects from the [Messier Catalog](https://en.wikipedia.org/wiki/Messier_object). The dataset includes basic information about each object, like it's type, magnitude, distance, constellation, and the best viewing season. Your tasks will involve reading the data, analyzing it, and using `numpy`, logic, and loops to answer questions about it! 

## Opening the Dataset

The data is stored in a `.npy` file, which you can load with `np.load()`. You can download it [here](./messier_data.npy) (right click and save as a `.npy` file). You can use the following line of code to open up the file in your code and store it's contents in a variable called `data`. 

```
data = np.load('/Users/username/Downloads/messier_data.npy')
```

Will the above line run on your computer? No! You need to update the PATH to match where the data lives on your computer! You can put the data anywhere on your computer, and specify the absolute PATH in your code like the example above. Alternately, if you put the data in the **same directory** (folder) as the python script you are writing, you can open it like this: `np.load(messier_data.npy)`.  

Each row in the dataset corresponds to a single Messier object, with the following fields:
- **Messier**: Name of the Messier object as a string (e.g., `'M107'`, `'M108'`)
- **RA** and **DEC**: the Right Ascension and Declination of the object (coordinates in the sky). 
- **Type**: Type of object (e.g., `'Gc'` for Globular Cluster, `'Sp'` for Spiral, `'Ba'` for Barred Spiral)
- **Mag**: Magnitude (brightness) of the object. Magnitudes are a unit-less system, and lower numbers mean brighter objects! 
- **Distance**: Distance from Earth in units of light-years
- **Constellation**: The constellation in which the object resides
- **Season**: The best viewing season (spring, summer, autumn, winter)

Here are some tips and reminders for using large 2D datasets: 
1) You can access each row of the dataset using **indexing**. For instance, `data[0]` will return the first row of the array (aka all of the above column values for a single Messier object).
2) You can access each column of the dataset using `data['Messier']` for example, where now rather than indexing by an integer we are indexing by a column **key** (a column name). This will return a numpy array of all the Messier numbers for all of the objects. 

# Exercise One: Overview Analysis of the Messier Catalog 

1. **How many objects are in the dataset?** You can either write a loop to count the number of objects or use a built-in python function. 

2. **Investigate the brightness of Messier objects:** Recall that magnitude is a measure of brightness, and brighter objects have lower magnitude values!
    - Calculate the average magnitude of all the Messier objects.
    - What magnitude is the brightest object in the catalog, and what magnitude is the dimmest?
    - Once you have that, calculate the difference in magnitude between the brightest and the dimmest object.

3. **How many objects are there in each viewing season** (spring, summer, autumn, winter)? Before looking at the hint, see if you can approach this problem on your own!

# Exercise Two: Getting More Practice  

1. Calculate the **average distance** of **spiral galaxies** (Type: `'Sp'`), **globular clusters** (Type: `'Gc'`), and **open clusters** (Type: `'Oc'`). Which type of object is typically farther away? Does this make sense?

2. **How many constellations are there in the dataset**, and **how many objects belong to each constellation?**
    - First, you need to find how many unique constellations exist in the dataset.
    - Then, count how many Messier objects belong to each constellation.

3. **How many Messier objects are in the northern vs. southern sky?** You could try to do this using the constellation information from the previous problem, but the hemisphere can more easily be determined by the **declination**.  
