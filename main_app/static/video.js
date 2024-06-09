console.log('hello world')

const video = document.getElementById('video-element')

if(navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video : true})
    .then((stream)=>{
        video.srcObject = stream
        })
}