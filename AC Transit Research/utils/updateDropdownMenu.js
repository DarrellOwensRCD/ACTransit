function generateOptions(route_names, route_info) {
     /*
        Function takes a list of values "1, 2, 3, 4, ..." and will use them as keys
        in the dictionary to retrieve route information "Arlington Blvd", "E. 14th Street" etc. 
        as keys to return for the dropdown menu
     */
    // Create an empty array to store the generated options
    let options = [];
    // Iterate over the elements of the input lists
    for (let i = 0; i < route_names.length; i++) {
        // Create an object with 'value' and 'label' properties
        let option = {
            value: route_names[i],
            label: route_info[route_names[i]][0] // 0 : Route Description, 1: Route Color 
        };
        // Push the object to the options array
        options.push(option);
    }
    return options;
}
