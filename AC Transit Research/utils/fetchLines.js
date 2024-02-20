const txtUrl = 'https://raw.githubusercontent.com/DarrellOwensRCD/ACTransit/master/AC%20Transit%20Research/Fall2023/gtfs/routes.txt';
// Function to fetch Transbay, Local and School lines, in 3 seperate lists, with each element being a tuples of (route,color), 
// passed within one list in order [L, T, S]
function isNumeric(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
}
function containsAlphaNumeric(str) {
    // Regular expression pattern to match both alphabetical and numerical characters
    var alphaNumericPattern = /^(?=.*[a-zA-Z])(?=.*[0-9])/;
    return alphaNumericPattern.test(str);
}
async function fetchLines() {
  try {
    const response = await fetch(txtUrl);
    const txt_data = await response.text();

    // Split the txt data into rows
    const rows = txt_data.split('\n');
    // Remove headers
    rows.shift();
    // Array to store list items
    const local = [];
    const transbay = [];
    const school = [];
    const owl = [];
    const early = []
    // Iterate through rows and create dictionary pairs
    rows.forEach(row => {
      const keys = row.split(',');
      if (keys[0].length === 3 && keys[0][0] === '6'){
        //School Route 800 series
        school.push(keys);
      }
      else if (keys[0].length === 3 && keys[0][0] === '7'){
        early.push(keys);
      }
      else if  (keys[0].length === 3 && keys[0][0] === '8'){
        owl.push(keys)
      }
      else if (keys[0] === '1T' || containsAlphaNumeric(keys[0]) || isNumeric(keys[0])) {
        //Local Line
        local.push(keys);
      }
      else{
        //Transbay Route
        transbay.push(keys);
      }
    });
    var complete_list = [local, transbay, school, owl, early];
    return complete_list;
  } catch (error) {
    console.error('Error fetching or processing AC Transit lines textfile:', error);
    return NULL;
  }
}
