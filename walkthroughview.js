import Notification from "./notification.js"
import { Viewer,EquirectangularAdapter  } from '@photo-sphere-viewer/core';
import { MarkersPlugin } from '@photo-sphere-viewer/markers-plugin';


export default  class View extends Notification{


    markers = {}

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

            this.markersPlugin = this.psviewer.getPlugin(MarkersPlugin);

            this.addMarker()


           
        })








    }


    addMarker(){

        this.markers  = {}


        console.log(this.psviewer)

        console.log(MarkersPlugin)

     

        console.log(this.markersPlugin)

        const neighbours  = this.data[this.spot];

        console.log(neighbours)

        neighbours.forEach(neighbour => {
            
            console.log(neighbour)

            const yaw = Common.degToRad(neighbour.sourceyaw)
            const pitch = Common.degToRad(neighbour.sourcepitch - 22.5)


            const mid = Common.makeid(10)

            this.markersPlugin.addMarker({



    
                position: { yaw: yaw, pitch: pitch},
                image : "marker.webp",
                anchor: 'bottom center',
                tooltip: 'Generated pin',
                data: {
                    generated: true,
                },
                size : {width: 50, height:50},
                id : mid

              
 
            })

            this.markers[mid] = neighbour


        });

        this.markersPlugin.addEventListener('select-marker', async ({ marker }) => {
           
           
            console.log('Clicked marker ID:', marker.id);

            const mdata = this.markers[marker.id]

            console.log(mdata)


            await  this.psviewer.animate({

                yaw : Common.degToRad(mdata.sourceyaw),
                pitch : Common.degToRad(mdata.sourcepitch),
                speed : 300

            })

            console.log("roate finish")


            await this.psviewer.animate({

                    zoom : 50,
                    speed : 300
    
            })

           console.log("zoomfinish")


             const photolink = `${this.filepath}/${mdata.targetspot}.jpg`

             this.markersPlugin.clearMarkers()

            
            await this.psviewer.setPanorama(photolink,{

                zoom : 0
            })
           




          });




    }





}