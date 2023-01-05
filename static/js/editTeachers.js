$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    //append table with 'add row' form when 'add new' button is clicked
    $(".add-new").click(function(){
        $(this).attr("disabled", "disabled");
        var index = $("table tbody tr:last-child").index();
        var row = '<tr>' +
            '<td><input type="text" class="form-control" name="teacherName" id="teacherName"></td>' +
            '<td><input type="text" class="form-control" name="teacherEmail" id="teacherEmail"></td>' +
        '<td>' + actions + '</td>' +
        '</tr>';
        $("table").append(row);  
        $("table tbody tr").eq(index + 1).find(".add, .edit, .delete").toggle();
        $('[data-toggle="tooltip"]').tooltip();
    });
   
    //adds a row to the form when 'add new' button is clicked
    $(document).on("click", ".add", function(){
        var empty = false;
        var input = $(this).parents("tr").find('input[type="text"]');
        input.each(function(){
            if(!$(this).val()){
                $(this).addClass("error");
                empty = true;
            } else{
                $(this).removeClass("error");
            }
        });
        //adds the following components in new row
        var teacherName = $("#teacherName").val();
        var teacherEmail = $("#teacherEmail").val();
        $.post("/ajax_add", { teacherName: teacherName, teacherEmail: teacherEmail}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
            var msg = data;
        });
        //co-ordinates with Flask app where it is checked if the user already has the inputted teacher linked to their account
        $(this).parents("tr").find(".error").first().focus();
        if(!empty && msg != "This teacher is already linked to this account"){
            input.each(function(){
                $(this).parent("td").html($(this).val());
            });   
            $(this).parents("tr").find(".add, .edit").toggle();
            $(".add-new").removeAttr("disabled");
        } 
    });
    //delete row when 'delete' button is clciked
    $(document).on("click", ".delete", function(){
        $(this).parents("tr").remove();
        $(".add-new").removeAttr("disabled");
        var id = $(this).attr("id");
        var string = id;
        $.post("/ajax_delete", { string: string}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        });
    });
    //the newly inputted information is updated in the database when the 'update' button is clicked
    $(document).on("click", ".update", function(){
        var id = $(this).attr("id");
        var string = id;
        var teacherName = $("#teacherName").val();
        var teacherEmail = $("#teacherEmail").val();
        $.post("/ajax_update", {string:string, teacherName: teacherName,teacherEmail: teacherEmail}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        });
         
         
    });
    //the user can edit the row information when the 'edit row' button is clicked
    $(document).on("click", ".edit", function(){  
        $(this).parents("tr").find("td:not(:last-child)").each(function(i){
            if (i=='0'){
                var idname = 'teacherName';
            }else if (i=='1'){
                var idname = 'teacherEmail'; 
            }else{} 
            $(this).html('<input type="text" name="updaterec" id="' + idname + '" class="form-control" value="' + $(this).text() + '">');
        });  
        $(this).parents("tr").find(".add, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");
        $(this).parents("tr").find(".add").removeClass("add").addClass("update"); 
    });
});