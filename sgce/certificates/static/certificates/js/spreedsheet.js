var
  tpl = [],
  save = document.getElementById('save'),
  hot;

function isEmptyRow(instance, row) {
  var rowData = instance.countRows();

  for (var i = 0, ilen = rowData.length; i < ilen; i++) {
    if (rowData[i] !== null) {
      return false;
    }
  }

  return true;
}

function defaultValueRenderer(instance, td, row, col, prop, value, cellProperties) {
  var args = arguments;

  if (args[5] === null && isEmptyRow(instance, row)) {
    args[5] = tpl[col];
    td.style.color = '#999';
  }
  else {
    td.style.color = '';
  }
  Handsontable.renderers.TextRenderer.apply(this, args);
}

hot = new Handsontable(document.getElementById('spreedsheet'), {
  startRows: 2,
  startCols: 1,
  minSpareRows: 1,
  contextMenu: true,
  rowHeaders: true,
  colHeaders: true,
  stretchH: 'all',
  width: 918,
  autoWrapRow: true,
  height: 487,
  colHeaders: ['Selecione um Modelo'],
  cells: function (row, col, prop) {
    var cellProperties = {};

    cellProperties.renderer = defaultValueRenderer;

    return cellProperties;
  },
  beforeChange: function (changes) {
    var instance = hot,
      ilen = changes.length,
      clen = instance.countCols(),
      rowColumnSeen = {},
      rowsToFill = {},
      i,
      c;

    for (i = 0; i < ilen; i++) {
      // if oldVal is empty
      if (changes[i][2] === null && changes[i][3] !== null) {
        if (isEmptyRow(instance, changes[i][0])) {
          // add this row/col combination to cache so it will not be overwritten by template
          rowColumnSeen[changes[i][0] + '/' + changes[i][1]] = true;
          rowsToFill[changes[i][0]] = true;
        }
      }
    }
    for (var r in rowsToFill) {
      if (rowsToFill.hasOwnProperty(r)) {
        for (c = 0; c < clen; c++) {
          // if it is not provided by user in this change set, take value from template
          if (!rowColumnSeen[r + '/' + c]) {
            changes.push([r, c, null, tpl[c]]);
          }
        }
      }
    }
  }
});

Handsontable.dom.addEvent(save, 'click', function() {
  // save all cell's data
  var input = $("<input>").attr("type", "hidden").attr("name", "certificates").val(JSON.stringify(hot.getData()));
  $('#form').append($(input));
  $('#form').submit();
});

function updateHeaders() {
    pk = document.getElementById("id_template").value;
    if (pk) {
        $.ajax({
          url: "/certificates/certificates/ajax/template/header/"+pk+"/",
          success: function(result){
              headers = result.headers;
              colHeaders = []
              columns = []
              for (var key in headers) {
                colHeaders.push(headers[key]);
                columns.push({})
              }
              hot.updateSettings({
                colHeaders: colHeaders,
                columns: columns,
              });
          }
        });
    } else {
        hot.updateSettings({
          colHeaders: ['Selecione um Modelo'],
          columns: [{}],
          data : [],
        });
    }
}

$( "#id_template" ).change(function() {
  updateHeaders();
});

$(document).ready(function() {
  updateHeaders();
});