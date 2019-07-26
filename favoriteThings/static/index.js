$(document).ready(function () {
    $("#addCategory").click(function () {
        var newCategory = $("#newCategory").val()
        var rate = $("#rate").val()
        console.log(rate,"rate")
        // add new Category to Category table
        $.ajax({
            url: '/createCategory',
            type: "POST",
            data: { category: newCategory,rate:rate },
            dataType: 'json',
            success: function (d) {
                $(function () {
                    $('#createCategory').modal('toggle');
                    $("#newCategory").val("")
                });
                $("#category").append(new Option(newCategory, newCategory));
            }
        })
    });
});