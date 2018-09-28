$('#clicking').on('click', function(){
    alert("you clicked the button!");
});

$('#btnGenerate').on('click', function(){
    $('#result').html($('#exampleInputEmail1').val());
    // alert("you clicked the button!");
});