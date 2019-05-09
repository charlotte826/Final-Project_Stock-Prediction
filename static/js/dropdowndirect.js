var fld = document.getElementById('d3-dropdown');
    var values = [];

   d3.select("select")
  .on("change",function(d){
    var thead1=d3.select("thead")
    thead1.html("")
    body1.html("")
    var values = [];
   for (var i = 0; i < fld.options.length; i++) {
  if (fld.options[i].selected) {
    values.push(fld.options[i].value);
    console.log(fld.options[i].value)
  }
}