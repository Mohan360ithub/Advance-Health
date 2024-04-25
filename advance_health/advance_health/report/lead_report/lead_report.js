// Copyright (c) 2024, pankaj@360ithub.com and contributors
// For license information, please see license.txt

frappe.query_reports["Lead Report"] = {
	"filters": [

	]
};

var previousSelectedRow = null;
 
document.addEventListener('click', function(event) {
    var cellContent = event.target.closest('.dt-cell__content');
 
    if (cellContent) {
        var row = cellContent.closest('.dt-row');
 
        if (previousSelectedRow) {
            var cellsInPreviousRow = previousSelectedRow.querySelectorAll('.dt-cell__content');
            cellsInPreviousRow.forEach(function(cellInRow) {
                cellInRow.style.backgroundColor = '';
            });
        }
 
        var cellsInRow = row.querySelectorAll('.dt-cell__content');
        cellsInRow.forEach(function(cellInRow) {
            cellInRow.style.backgroundColor = '#D3D3D3';
        });
 
        previousSelectedRow = row;
    }
});
