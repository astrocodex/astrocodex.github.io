import time
import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures

def load_data(i):
    """
    a mappable function to load in the ith image.
    
    Args:
    i - int - index
    
    Returns:
    image_i - np.ndarray - a (256,256) image array corresponding to index i.
    """
    
    time.sleep(0.01) #artificial sleep to mimick the scenario
    image_i = plt.imread(f'./images/{i}.jpg')
    
    return image_i

def main():

    max_workers = 4 #this should be however many cores you are able to use

    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        images = list(executor.map(load_data, range(1000)))
        executor.shutdown(wait=True)
    stop = time.time()  
    print(f"Loading in the data took ~{stop - start:0.2f} seconds")
        
    return images
        
if __name__ == '__main__':
    images = main()
    """ 
    from here the list of images can be used as one 
    pleases. It can be fed into other functions for 
    analysis for example. For this example, we
    will just save them all into large numpy array 
    and save that array to local storage.
    """
    images = np.array(images)
    np.save('images.npy', images)
    
