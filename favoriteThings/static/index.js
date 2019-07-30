$(document).ready(function () {
    $("#addCategory").click(function () {
        var newCategory = $("#newCategory").val()
        var rate = $("#rate").val()
        // add new Category to Category table
        $.ajax({
            url: '/createCategory',
            type: "POST",
            data: { category: newCategory,rate:rate },
            dataType: 'json',
            success: function (res) {
                if(res.success){

                    $(function () {
                        $('#createCategory').modal('toggle');
                        $("#newCategory").val("")
                    });
                    $("#category").append(new Option(newCategory, newCategory));
                }else{
                    $('#createCategory').modal('toggle');
                    $("#error").append('<div class="alert alert-danger">'+ res.error +'</div>')
                }
            }
        })
    });
    $("#addField").click(function () {
        var name = $("#fieldName").val()
        var type = $("#type").val()
        if(name){
            $("#fieldName").val("")
            $(".Fields").append('<div> <label class="form-control-label" for="'+name+'">\
            '+ name +'</label>\
                                             <input required class="form-control" type="'+ type + '" name='+ type +'-meta-'+ name + ' id="'+ name+'"></div>')
        }
        

    });
});