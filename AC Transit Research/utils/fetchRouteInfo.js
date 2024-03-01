function generateRoutes(){
  // URL of the comma-delimited text file on GitHub
  const fileUrl = 'https://raw.githubusercontent.com/DarrellOwensRCD/ACTransit/master/AC%20Transit%20Research/Fall2023/gtfs/routes.txt';

  // Initialize an empty dictionary to store the data
  let dataDictionary = {};

  // Fetch the data from the URL
  fetch(fileUrl)
    .then(response => response.text())
    .then(data => {
      // Split the data into lines
      let lines = data.split('\n');

      // Iterate through each line
      lines.forEach(line => {
        // Split the line into columns using comma as the delimiter
        let columns = line.split(',');

        // Check if the line has at least 3 columns
        if (columns.length >= 3) {
          // Store the 1st and 3rd columns into the dictionary
          let key = columns[0].trim(); // Assuming the key is in the 1st column
          let value = [columns[3].trim(),columns[7].trim()]; // Assuming the value is in the 3rd column

          // Store key-value pair in the dictionary
          dataDictionary[key] = value;
        }
      });

      // Output the dictionary
      console.log(dataDictionary);
      console.log("You fucking working?")
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}