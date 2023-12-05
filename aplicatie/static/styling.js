$(document).ready(function() {
    $("#flashMessage").delay(5000).slideUp(300);
    // Use a single key for all the table data
var TABLE_DATA_KEY = 'tableData';

// Load the table data from local storage
var tableData = JSON.parse(localStorage.getItem(TABLE_DATA_KEY)) || {};

// Update the table with the data from local storage
$("tr").each(function(index){
    var rowKey = TABLE_DATA_KEY + index; // Create a unique key for each row
    var rowData = JSON.parse(localStorage.getItem(rowKey)) || {};

    if(rowData){
        $(this).children().each(function(){
            $(this).text(rowData[$(this).index() - 1]); // Subtract 1 from the index here
        });
    }
});

// Make table cells editable
$("td.editabil").attr("contenteditable", "true");

// Save the new value when a cell loses focus
$("td").blur(function(){
    var cell = $(this);
    var row = cell.parent();
    var rowId = row.attr('id'); // Use the row ID as the key

    // Get the row data from the table data, or create a new object if it doesn't exist
    var rowData = tableData[rowId] || (tableData[rowId] = {});

    // Update the cell value in the row data
    rowData[cell.attr('id')] = cell.text(); // Use the cell ID instead of index

    // Try to save the table data in local storage
    try {
        localStorage.setItem(rowId, JSON.stringify(rowData)); // Use rowId instead of rowKey
    } catch(e) {
        console.error('Failed to save table data in local storage:', e);
    }
 
    // Send the new value to the server
    $.ajax({
        url: '/update_contract',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            rowId: rowId,
            columnIndex: cell.index(),
            newValue: cell.text()
        }),
        success: function(response) {
            console.log(response);
        }
    });
    
    
});

    var $rows = $("tr");
    var $cells = $("td");
    
    $cells.keydown(function(e){
        var key = e.which;
        var $this = $(this);
        var colIndex = $this.index();
        var rowIndex = $this.closest('tr').index();
        var text = $this.text().trim(); // Trim trailing spaces and line breaks
        var cursorPosition = window.getSelection().getRangeAt(0).startOffset;
    
        switch(key){
            case 37: // Left arrow
                if(cursorPosition === 0 && colIndex > 0) {
                    $rows.eq(rowIndex).find('td').eq(colIndex - 1).focus();
                }
                break;
            case 38: // Up arrow
                if(rowIndex > 0) {
                    $rows.eq(rowIndex - 1).find('td').eq(colIndex).focus();
                }
                break;
            case 39: // Right arrow
                if(cursorPosition === text.length && colIndex < $rows.eq(rowIndex).find('td').length - 1) {
                    $rows.eq(rowIndex).find('td').eq(colIndex + 1).focus();
                }
                break;
            case 40: // Down arrow
                if(rowIndex < $rows.length - 1) {
                    $rows.eq(rowIndex + 1).find('td').eq(colIndex).focus();
                }
                break;
        }
    });

    function titluTable(s) {
        s = s.replace(/([A-Z])/g, ' $1').trim(); // Adăugați un spațiu înainte de fiecare literă mare
        return s.charAt(0).toUpperCase() + s.slice(1); // Transformați prima literă în literă mare
    }    
    $(".titluTabel").each(function() {
        var text = $(this).text();
        text = titluTable(text);
        $(this).text(text);
    });  


// localStorage.clear(); // -> important daca vrei sa stergi greselile de pana acum 
});

