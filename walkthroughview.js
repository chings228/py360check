import Notification from "./notification.js"
import { Viewer,EquirectangularAdapter  } from '@photo-sphere-viewer/core';
import { MarkersPlugin } from '@photo-sphere-viewer/markers-plugin';


export default  class View extends Notification{


    constructor(data){

        super()
        this.data = data


        this.filepath = `photo_home1`
        this.spot = "fcd81es2iht9aexpk38fgurha"

  

        console.log(this.filepath)
        console.log(MarkersPlugin)


        this.init()
    }




    init(){


       const photolink = `${this.filepath}/${this.spot}.jpg`

        this.psviewer  =new Viewer({

            container: document.querySelector(".psview"),
            panorama: photolink,
            defaultZoomLvl : 0,

            adapter: [EquirectangularAdapter, {
                useXmpData: false // Disables reading GPano XMP orientation metadata
            }],
            navbar : false,
            plugins: [
                [MarkersPlugin, {
                    // Optional configuration options here
                }]
            ]



        })


        this.psviewer.addEventListener("ready",e=>{


            console.log("ready")

            this.addMarker()
        })



        const markersPlugin = this.psviewer.getPlugin(MarkersPlugin);





    }


    addMarker(){


        console.log(this.psviewer)

        console.log(MarkersPlugin)

        const markersPlugin = this.psviewer.getPlugin(MarkersPlugin);

        console.log(markersPlugin)

        const neighbours  = this.data[this.spot];

        console.log(neighbours)

        neighbours.forEach(neighbour => {
            
            console.log(neighbour)

            const yaw = Common.degToRad(neighbour.sourceyaw)
            const pitch = Common.degToRad(neighbour.sourcepitch - 22.5)


            markersPlugin.addMarker({



    
                position: { yaw: yaw, pitch: pitch},
                image : "marker.webp",
                anchor: 'bottom center',
                tooltip: 'Generated pin',
                data: {
                    generated: true,
                },
                size : {width: 50, height:50},
                id : "sdfsdf"
            });


        });



    }





}