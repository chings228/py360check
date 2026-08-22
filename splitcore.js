


import { Viewer,EquirectangularAdapter  } from '@photo-sphere-viewer/core';

import { MarkersPlugin } from '@photo-sphere-viewer/markers-plugin';



export default class splitcore{

    stitch 

    pictures = []


    constructor(){



        console.log("hahaxxx")


        $.getJSON("./data.json",e=>{

            console.log(e)
            this.stitch = e

            this.init()


        })

    }


    init(){

        for (const key in this.stitch){

            this.pictures.push(key)


        }

        console.log(this.pictures)

        this.startUI()


    }



    startUI(){


        this.UISelectBar()

        this.UIPhotoView()

        this.UIConnectedDetail()

    }


    UISelectBar(){

        const ele = $(".splitdiv .selectbar")


        let html = `<select class=pictureselect>`

        this.pictures.forEach((pic) => {

            html += `<option = ${pic}>${pic}`
            
        });

        html +=`</select>`


        ele.append(html)



        $(".pictureselect").change(e=>{

            console.log(e)

            const type = $(e.currentTarget).parent().parent().parent().attr('id')

            console.log(type)

            const param = {}
            param.type = type
            param.img = e.currentTarget.value

            this.handleChangeImg(param)
        })

    }

    UIConnectedDetail(){

        const types = ['source','target']


        types.forEach(e=>{

            let typeid = this.sourceId

            if (e == 'target'){
                typeid = this.targetId
            }

            console.log(typeid)

            const sublist = this.stitch[typeid]

            const ele = $(`#${e} .splittext .detail`)

            let html = `Connected Sweep<br>`

            for (const pic in sublist){

                const detail = this.stitch[typeid][pic]
                const yaw_angle = detail.yaw_angle
                const inliers = detail.inliers
                const goodmatch = detail['good matches']


                html += `${pic} <br>yaw ${yaw_angle} inliers ${inliers}  matches ${goodmatch}<br><br>`
            }

            console.log(`connected ${html} `)

            ele.html(html) 


        })



    }


  getUrlParameter(sParam) {

        console.log("geturl",sParam)
          var sPageURL = window.location.search.substring(1);
          var sURLVariables = sPageURL.split('&');
    
          for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
    
            var key = sParameterName[0];
    
            if (key == sParam) {
              return sParameterName[1];
            }
          }
        }


        degToRad(angle){

            return angle * Math.PI / 180
        }


    UIPhotoView(){

        this.sourceId = this.pictures[0]
        this.targetId = this.pictures[0]


        if (this.getUrlParameter('source')){
            this.sourceId = `${this.getUrlParameter('source')}.jpg`
        }

        if (this.getUrlParameter('target')){
            this.targetId= `${this.getUrlParameter('target')}.jpg`
        }



        if (this.getUrlParameter('sourceyaw')){
            this.sourceyaw = `${this.getUrlParameter('sourceyaw')}`
        }

        if (this.getUrlParameter('targetyaw')){
            this.targetyaw = `${this.getUrlParameter('targetyaw')}`
        }


        console.log(`source yaw ${this.sourceyaw} ${this.degToRad(this.sourceyaw)}`)


        this.sourceviewer = new Viewer({
            container: document.querySelector('#sourceviewer'),
            panorama: `scene1/${this.sourceId}`,
            defaultZoomLvl : 0,
            defaultYaw : this.degToRad(this.sourceyaw),
            adapter: [EquirectangularAdapter, {
                useXmpData: false // Disables reading GPano XMP orientation metadata
            }],
            navbar : false
        });

        this.targetviewer = new Viewer({
            container: document.querySelector('#targetviewer'),
            panorama: `scene1/${this.targetId}`,
            defaultZoomLvl : 0,
            defaultYaw : `${this.degToRad(this.targetyaw)}`,
            adapter: [EquirectangularAdapter, {
                useXmpData: false // Disables reading GPano XMP orientation metadata
            }],
            navbar : false
        });


        

        this.sourceviewer.addEventListener('position-updated',position=>{

            const param = {}
            param.type = 'source'
            param.position = position

            this.handlePositionListener(param)

        })
        this.targetviewer.addEventListener('position-updated',position=>{

            const param = {}
            param.type = 'target'
            param.position = position

            this.handlePositionListener(param)

        })


    }

    handlePositionListener(e){

            const position = e.position.position

            const yaw = position.yaw * 180 / Math.PI
            const pitch = position.pitch

            const text = `yaw ${yaw} pitch ${pitch}`

            $(`#${e.type} .splittext .position`).html(text)




          


    }


    handleChangeImg(e){

        let viewer = this.sourceviewer

        if (e.type == 'target'){
            viewer  =  this.targetviewer

            this.targetId = e.img
        }
        else{
            this.sourceId = e.img
        }

        viewer.setPanorama(`scene1/${e.img}`)

        this.UIConnectedDetail()

    }

}