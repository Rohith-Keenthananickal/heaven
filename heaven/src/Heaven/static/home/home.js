// $(document).ready(function() {
//     window.location.href('/upload')
// });
$(window).on('load', function(){ 
    
});
$(document).ready(function() {
    $('#create-btn').on("click",()=>{
        console.log("work");
        window.location.href = 'http://127.0.0.1:8000/upload';
    });

    
});

function getId(id){
    console.log(id);
    localStorage.setItem("id", id);
}