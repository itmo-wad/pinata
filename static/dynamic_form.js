document.getElementById("addDynamicExtraFieldButton").onclick = function(event) {
	event.preventDefault();
	let div = document.createElement("div");
	div.className = "DynamicExtraField";
	$("<br>").appendTo(div);
    $('<input/>', {value : 'Remove item', type : 'button', 'class' : 'DeleteDynamicExtraField'}).appendTo(div).click(function(e) {
		$(this).parent().remove();
		e.preventDefault();
		return false;
	});  
	$('<br>').appendTo(div);
	$('<br>').appendTo(div);
	$('<p>').appendTo(div);
	$('<label/>', {for : "item"}).html("Item name ").appendTo(div); //	<label for="item">Item name:</label>
	$('<input/>', {name : 'item-title[]', type : 'text', id : 'item', required :''}).appendTo(div);// <input type="text" name="item-title[]" id="item">
	$('<label/>', {for : "link"}).html(" Reference ").appendTo(div); //	<label for="link">Reference:</label>
	$('<input/>', {name : 'item-link[]', type : 'text', placeholder : " Link to shop website", id : 'link' }).appendTo(div);	// <input type="text" name="item-link[]" id="link" placeholder="Input link to store">
	$('</p>').appendTo(div);
	$('<p>', {class: 'textform'}).html("Input description for your new item").appendTo(div);
	$('</p>').appendTo(div);
    $('<p>').appendTo(div);
	$('<textarea/>', {name : 'item-descr[]', cols : '50' }).appendTo(div);
	$('<br>').appendTo(div);
	$('<input/>', {name : 'file[]', type : 'file', class: 'forma'}).appendTo(div); // <input type="file" name="file[]">
	$('</p>').appendTo(div);
	$('<hr>').appendTo(div);
	$('<br>').appendTo(div);
 //Добавляем уже собранный DIV в DynamicExtraFieldsContainer
	$(div).appendTo("#DynamicExtraFieldsContainer");
	
};