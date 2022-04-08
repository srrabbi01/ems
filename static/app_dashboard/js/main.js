(function ($) {

	"use strict";

	var fullHeight = function () {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function () {
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();



})(jQuery);


document.addEventListener('change', function () {
	var file_size = "";
	var valid_size = 1048576 * 5;
	var file = document.getElementById("id_files");
	var label = document.getElementById("filelabel");

	if (file && file.files.length != 0) {
		file_size = file.files[0].size;
		if (file_size > valid_size) {
			label.classList.add('errorlabel')
			label.innerHTML = '* Maximum File Size Exceeded. Selected File is Over 5MB';
			file.value = null
			$("#create").addClass('disabled');
		} else {
			label.classList.remove('errorlabel')
			label.innerHTML = 'Maximum upload file size: 5MB';
			$("#create").removeClass('disabled');
		}
	}
})

$("#id_priority option:first").html('Please Select');




$('.review').on('click', function () {
	let this_parent = $(this).closest('tr');
	let title = this_parent.children()[1].textContent;
	$('input[name="service_id"]').val(this_parent.data('serviceId'));
	$('#serviceName').text(title);
	$.featherlight('.modal-form');
});



$(document).ready(function () {
	$('#table_data').DataTable();
});


$(document).ready(function () {
	$('#paymnets-table').DataTable();
	$('.pagination').addClass('pagination-sm')

});