$(document).ready(function(){
    let sel = $("#video-player");
    
    // Use .attr() to get the attribute value in jQuery
    let videoId = localStorage.getItem("id");
    
    // Use console.log to output the videoId
    console.log(videoId);
    
    const startByte = 0;  // Specify the starting byte
    const endByte = 999;  // Specify the ending byte

    const headers = {
        Range: `bytes=${startByte}-${endByte}`
    };

    $.ajax({
        url: `http://127.0.0.1:8000/id/${videoId}/`,
        type: 'GET',
        headers: headers,
        success: function (data, status, xhr) {
            if (xhr.status === 206) {
                // Handle the partial content response
                const blob = new Blob([data], { type: 'video/mp4' });
                console.log(blob);
                const videoPlayer = document.getElementById('video-player');
                videoPlayer.src = URL.createObjectURL(blob);
            } else {
                // Handle other responses
                console.error('Unexpected response status:', xhr.status);
            }
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
        }
    });



    // var player = videojs('my-video');
    // var seekTime = 30; // Set this to the desired seek time
    //     player.currentTime(seekTime);

    //     // Set preload option
    //     var preloadOption = 'metadata'; // 'none', 'metadata', or 'auto'
    //     player.preload(preloadOption);
})

