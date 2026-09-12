
import Notification from "./notification.js"
import { Viewer,EquirectangularAdapter  } from '@photo-sphere-viewer/core';


export default class View extends Notification{




    constructor(data){

        super()


        console.log(data)
        this.type = data.type

        this.spots = data.spots
        this.code = data.code

        this.filepath = `photo_${data.code}`

        this.yaw = 0
        this.pitch  = 0
        this.spot = this.spots[0]


        this.init()


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
            const spot = $(e.target).val()

            console.log(spot)

            this.changePhoto(spot)

        })


        const photolink = `${this.filepath}/${this.spot}.jpg`
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
            // console.log(`rad ${Common.dformat(position.pitch)},${Common.dformat(position.yaw)}`)

            this.yaw = Common.dformat(Common.radToDeg(position.yaw))

            this.pitch = Common.dformat(Common.radToDeg(position.pitch))

            // console.log(`deg  yaw ${this.yaw}  pitch ${this.pitch}`)

            const text = ` Rad : yaw ${position.yaw} pitch ${position.pitch}
            <br>
            Deg : yaw : ${this.yaw} pitch ${this.pitch}
            
            `


            $(`#${this.type} .datadiv`).html(text)

        })



    }


    changePhoto(spot){

            this.spot = spot

            const link = `photo_${this.code}/${spot}.jpg`

            this.psviewer.setPanorama(link)



            const plaindivhtml = `<img src=${link} width = 100%>`

            $(`#${this.type} .plaindiv`).html(plaindivhtml)



    }



}