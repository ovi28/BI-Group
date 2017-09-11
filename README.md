## List of files: price_list.csv, price_list.txt, prices.png

## Types: a csv file, a txt file and an image with the format png

## The output: 3307228.119047619

## Lines 1-8: importing the necessary libraries
   The matplotlib.use('agg') line is for saving stuff to file and not display it on screen

Lines 11-14 This method has two parameters: a url and a path where a file should be saved. It’s making a request to the url and getting the request from it and saving it on the local machine.

Lines 17-38 This method generates a .CSV(comma separated value) file. It takes two parameters: location of a file where it should get the values from and where it should save the CSV file. Lines 18 and 19 are responsible to open the text file, reading it line by line and saving it into a variable for later use. The first line of the CSV file is saved in the rows variable and then in the for loop from lines 22-29 it’s adding the values to the rows variable one line at a time. Lines 30-33 are responsible for using the right type of newline for Windows or Unix. The last part of the method creates the csv file and writes to it the values from the rows variable.

Lines 41-53 This method returns a list with all the prices from a csv file gotten from the parameter. First of all, it opens the file and then it goes line by line adding the price from the 3rd column to the prices array. It returns a list with all the prices and the line numbers (represented as ids) on which they were found.

Lines 56-63 This method calculates the average price from a list received as a parameter. It calculates the average from the list using statistics.mean() and it writes it to a temporary files and returns it at the end.

Lines 66-71 This method generates an image file with a graph containing all the prices. The y axis is represented by the prices and the X axis by their id. Using plt.scatter() the graph is generated and then saved to a png file. The scatter method takes 3 parameters: the values for the X and Y axis and the size of the dots.

The run method is responsible for generating all the files. First of all, it saves a text file containing all the building information from a URL. After that it will initialize the name of the CSV file and generate it and save it to disk. It will then calculate the average price, print it and generate the png file with all the prices.
