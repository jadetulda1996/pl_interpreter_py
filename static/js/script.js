$('#clicking').on('click', function(){
    alert("you clicked the button!");
});

$('#btnGenerate').on('click', function(){
    //$('#result').html($('#exampleInputEmail1').val());
    var code = $('#editor').val();
    if(code.trim()) { //to check if editor is empty: .trim() is used to remove whitespaces
        $.ajax({
            type: "GET",
            url: "/interpreter/",
            data: { msg: code },
            //contentType: "application/json", 
            //dataType: 'json',
            async:false,        
            success: function(data, status){
                console.log("success python call....");
                $('#result').val(data);
            },
            error: function(xhr, desc, err){
                console.log("something went wrong...");
            }
        });
    } else {
        console.log("empty editor");
    }
});