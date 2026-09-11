
import Notification from "./notification.js"
import { Viewer,EquirectangularAdapter  } from '@photo-sphere-viewer/core';


export default class View extends Notification{


    constructor(data){

        super()


        console.log(data)
        this.type = data.type

        this.spots = data.spots

        this.filepath = `photo_${data.code}`




        this.init()


    }

    degToRad(angle){

        return angle * Math.PI / 180
    }

    radToDeg(angle){

        return angle * 180 / Math.PI
    }



    init(){

        let html = `
        
        <div class=spotoptiondiv>

        </div>

        <div class=plaindiv>

        </div>
        
        <div class= photodiv>

        </div>

        <div class = datadiv>

        yaw : 0  , pitch : 0

        </div>
        
        
        `


        $(`#${this.type}`).html(html)



        let optionhtml = ``

        this.spots.forEach(spot => {

            optionhtml += `<option pid = ${spot}>${spot}`
            
        })

    
        let selecthtml = `<select class=spotoption>${optionhtml}</select>`

        $(`#${this.type} .spotoptiondiv`).html(selecthtml)




        $(`#${this.type} .spotoption`).change(e=>{



            console.log("change",e)
            const type = $(e.target).val()

            console.log(type)

        })


        const photolink = `${this.filepath}/${this.spots[0]}.jpg`
        const containerStr = `#${this.type} .photodiv`

        console.log(containerStr)

        const plaindivhtml = `<img src=${photolink} width = 100%>`

        $(`#${this.type} .plaindiv`).html(plaindivhtml)



        this.psviewer = new Viewer({

            container: document.querySelector(containerStr),
            panorama: photolink,
            defaultZoomLvl : 0,

            adapter: [EquirectangularAdapter, {
                useXmpData: false // Disables reading GPano XMP orientation metadata
            }],
            navbar : false



        })



        this.psviewer.addEventListener('position-updated',e=>{

            console.log(this.type)
            const position = e.position
            console.log(position.pitch,position.yaw)
            console.log(this.radToDeg(position.pitch),this.radToDeg(position.yaw))

        })



    }



}