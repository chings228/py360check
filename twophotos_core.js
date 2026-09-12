
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


        this.submitbutton()



    }


    createView(){

        const data = {}
        data.spots = this.spots
        data.type = "source"
        data.code = this.code

        this.sourceView  = new View(data)

        data.type = "target"

        this.targetView = new View(data)




    }


    submitbutton(){



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







    }



}