
import View from "./twophotos_view.js";


export default class Core{



    constructor(){



        this.init()

    }






    init(){

        this.code = Common.getUrlParameter('code')

        console.log(this.code)



        $.getJSON(`fovresult-${this.code}.json`,data=>{


            this.spots = data.spotlist

            console.log(this.spots)

            this.createView()



        })


        this.button()



    }


    createView(){

        const data = {}
        data.spots = this.spots
        data.type = "source"
        data.code = this.code

        data.spot = this.spots[0]
        data.yaw = 0
        data.pitch = 0

        // init source

        

        if (Common.getUrlParameter('sourcespot')){


            data.spot = Common.getUrlParameter('sourcespot')
            data.yaw = Common.getUrlParameter('sourceyaw')
            data.pitch = Common.getUrlParameter('sourcepitch')

        }
       




        this.sourceView  = new View(data)

        
        
        
        // init target 

        if (Common.getUrlParameter('targetspot')){


            data.spot = Common.getUrlParameter('targetspot')
            data.yaw = Common.getUrlParameter('targetyaw')
            data.pitch = Common.getUrlParameter('targetpitch')
        }
        
        
        
        data.type = "target"

        this.targetView = new View(data)




    }


    button(){



        $("#btn_submit").click(e=>{

            console.log(this.sourceView)


            const param = {}



            param.sourcepitch = this.sourceView.pitch
            param.sourceyaw = this.sourceView.yaw
            param.sourcespot = this.sourceView.spot

            param.targetpitch = this.targetView.pitch
            param.targetyaw = this.targetView.yaw
            param.targetspot = this.targetView.spot

            param.method = "connect.php"
    
    
            console.log(param)

            Common.api(param)
            .then(e=>{

                console.log(e)

            })

        })



        $("#btn_swap").click(e=>{


            console.log("swap")

            const sourcephoto = this.sourceView.spot
            const targetphoto = this.targetView.spot

            this.sourceView.changePhoto(targetphoto)
            this.targetView.changePhoto(sourcephoto)

            



        })







    }



}