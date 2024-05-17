frappe.query_reports["Lead Follow Up Count Report"] = {
    "filters": [
 
        {
            "fieldname": "from_date",
            "label": __("Select The Date Range"),
            "fieldtype": "DateRange",
        }
    ],
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

